"""Orchestrates a full scan of a project's source tree: languages, LOC, large
files, dependencies, TODOs, secrets and complexity. This is the core analysis
engine used by the Celery workers.
"""
import os
from dataclasses import dataclass, field
from pathlib import Path

from app.services.complexity_analyzer import ComplexityResult, analyze_complexity
from app.services.language_detector import DEPENDENCY_FILES, IGNORED_DIR_NAMES, detect_language
from app.services.secret_scanner import SecretFinding, scan_text_for_secrets
from app.services.todo_scanner import TodoFinding, scan_text_for_todos

LARGE_FILE_THRESHOLD_BYTES = 500 * 1024  # 500KB
MAX_FILE_READ_BYTES = 2 * 1024 * 1024  # do not read files larger than 2MB as text
BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".gz", ".tar",
    ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".mp3", ".exe", ".dll", ".so",
    ".pyc", ".class", ".jar", ".bin", ".dat", ".db", ".sqlite",
}


@dataclass
class ScanResult:
    total_files: int = 0
    total_dirs: int = 0
    total_loc: int = 0
    languages: dict[str, int] = field(default_factory=dict)  # language -> LOC
    language_file_counts: dict[str, int] = field(default_factory=dict)
    dependencies: dict[str, str] = field(default_factory=dict)  # filename -> manager
    large_files: list[dict] = field(default_factory=list)
    todos: list[TodoFinding] = field(default_factory=list)
    secrets: list[SecretFinding] = field(default_factory=list)
    complexity: list[ComplexityResult] = field(default_factory=list)

    def to_summary_dict(self) -> dict:
        avg_complexity = (
            round(sum(c.complexity_score for c in self.complexity) / len(self.complexity), 2)
            if self.complexity
            else 0.0
        )
        return {
            "total_files": self.total_files,
            "total_dirs": self.total_dirs,
            "total_loc": self.total_loc,
            "languages": self.languages,
            "language_file_counts": self.language_file_counts,
            "dependencies": self.dependencies,
            "large_files": self.large_files[:50],
            "todo_count": len(self.todos),
            "todos": [t.__dict__ for t in self.todos[:200]],
            "secret_count": len(self.secrets),
            "secrets": [s.__dict__ for s in self.secrets[:100]],
            "average_complexity_score": avg_complexity,
            "most_complex_files": [
                c.__dict__ for c in sorted(self.complexity, key=lambda c: -c.complexity_score)[:20]
            ],
        }


def _is_probably_binary(path: Path) -> bool:
    return path.suffix.lower() in BINARY_EXTENSIONS


def scan_project(root_dir: str, progress_callback=None) -> ScanResult:
    """Walk the project tree and collect all analysis data.

    progress_callback(percent: int, message: str) is invoked periodically so
    the caller (a Celery task) can report progress back to the job record.
    """
    result = ScanResult()
    root = Path(root_dir)

    all_files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIR_NAMES]
        result.total_dirs += 1
        for filename in filenames:
            all_files.append(Path(dirpath) / filename)

    total = len(all_files) or 1

    for idx, file_path in enumerate(all_files):
        result.total_files += 1
        rel_path = str(file_path.relative_to(root))

        if file_path.name in DEPENDENCY_FILES:
            result.dependencies[rel_path] = DEPENDENCY_FILES[file_path.name]

        try:
            size = file_path.stat().st_size
        except OSError:
            size = 0

        if size > LARGE_FILE_THRESHOLD_BYTES:
            result.large_files.append({"path": rel_path, "size_bytes": size})

        if _is_probably_binary(file_path) or size > MAX_FILE_READ_BYTES or size == 0:
            if progress_callback and idx % 50 == 0:
                progress_callback(int(idx / total * 100), f"Processando {rel_path}")
            continue

        language = detect_language(file_path.name)

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except (OSError, UnicodeDecodeError):
            continue

        loc = len([l for l in content.splitlines() if l.strip()])
        result.total_loc += loc

        if language:
            result.languages[language] = result.languages.get(language, 0) + loc
            result.language_file_counts[language] = result.language_file_counts.get(language, 0) + 1
            if language not in ("JSON", "YAML", "Markdown", "XML", "TOML"):
                result.complexity.append(analyze_complexity(rel_path, content))

        result.todos.extend(scan_text_for_todos(rel_path, content))
        result.secrets.extend(scan_text_for_secrets(rel_path, content))

        if progress_callback and idx % 50 == 0:
            progress_callback(int(idx / total * 100), f"Processando {rel_path}")

    if progress_callback:
        progress_callback(100, "Varredura concluida")

    return result
