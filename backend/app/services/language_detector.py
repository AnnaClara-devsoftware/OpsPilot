"""Maps file extensions to human-readable language names."""

EXTENSION_LANGUAGE_MAP: dict[str, str] = {
    ".py": "Python", ".pyi": "Python",
    ".js": "JavaScript", ".jsx": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript",
    ".java": "Java", ".kt": "Kotlin", ".kts": "Kotlin",
    ".go": "Go", ".rs": "Rust", ".rb": "Ruby", ".php": "PHP",
    ".c": "C", ".h": "C", ".cpp": "C++", ".hpp": "C++", ".cc": "C++",
    ".cs": "C#", ".swift": "Swift", ".m": "Objective-C",
    ".html": "HTML", ".htm": "HTML", ".css": "CSS", ".scss": "SCSS", ".sass": "Sass",
    ".json": "JSON", ".yaml": "YAML", ".yml": "YAML", ".toml": "TOML", ".xml": "XML",
    ".md": "Markdown", ".sql": "SQL", ".sh": "Shell", ".bash": "Shell",
    ".dockerfile": "Docker", ".vue": "Vue", ".dart": "Dart", ".scala": "Scala",
    ".r": "R", ".lua": "Lua", ".pl": "Perl", ".ex": "Elixir", ".exs": "Elixir",
}

DEPENDENCY_FILES = {
    "requirements.txt": "pip", "pyproject.toml": "pip/poetry", "Pipfile": "pipenv",
    "package.json": "npm", "yarn.lock": "yarn", "pnpm-lock.yaml": "pnpm",
    "go.mod": "go modules", "Cargo.toml": "cargo", "pom.xml": "maven",
    "build.gradle": "gradle", "build.gradle.kts": "gradle", "Gemfile": "bundler",
    "composer.json": "composer",
}

IGNORED_DIR_NAMES = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
    ".next", ".pytest_cache", ".mypy_cache", "target", ".idea", ".vscode", "coverage",
}


def detect_language(filename: str) -> str | None:
    for ext, lang in EXTENSION_LANGUAGE_MAP.items():
        if filename.lower().endswith(ext):
            return lang
    return None
