"""Heuristic secret scanner: regex patterns for common credential formats."""
import re
from dataclasses import dataclass

PATTERNS: dict[str, re.Pattern] = {
    "AWS Access Key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "AWS Secret Key": re.compile(r"(?i)aws(.{0,20})?(secret|key)(.{0,20})?['\"][0-9a-zA-Z/+]{40}['\"]"),
    "Generic API Key": re.compile(r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]"),
    "Generic Secret": re.compile(r"(?i)(secret|token)\s*[:=]\s*['\"][A-Za-z0-9_\-\.]{16,}['\"]"),
    "Private Key Block": re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "Slack Token": re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}"),
    "GitHub Token": re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    "JWT-looking string": re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    "Password assignment": re.compile(r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"][^'\"\s]{6,}['\"]"),
    "Database URL with credentials": re.compile(r"(?i)(postgres|mysql|mongodb)(\+\w+)?://[^:]+:[^@]+@"),
}

MAX_LINE_LENGTH_TO_SCAN = 2000


@dataclass
class SecretFinding:
    file_path: str
    line_number: int
    rule_name: str
    snippet: str


def scan_text_for_secrets(file_path: str, content: str) -> list[SecretFinding]:
    findings: list[SecretFinding] = []
    for line_number, line in enumerate(content.splitlines(), start=1):
        if len(line) > MAX_LINE_LENGTH_TO_SCAN:
            continue
        for rule_name, pattern in PATTERNS.items():
            match = pattern.search(line)
            if match:
                snippet = line.strip()
                if len(snippet) > 120:
                    snippet = snippet[:117] + "..."
                findings.append(SecretFinding(file_path, line_number, rule_name, snippet))
    return findings
