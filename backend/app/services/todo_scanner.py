"""Scans source files for TODO / FIXME / HACK / XXX comments."""
import re
from dataclasses import dataclass

TODO_PATTERN = re.compile(r"(?i)\b(TODO|FIXME|HACK|XXX)\b[:\s]?(.*)")


@dataclass
class TodoFinding:
    file_path: str
    line_number: int
    tag: str
    text: str


def scan_text_for_todos(file_path: str, content: str) -> list[TodoFinding]:
    findings: list[TodoFinding] = []
    for line_number, line in enumerate(content.splitlines(), start=1):
        match = TODO_PATTERN.search(line)
        if match:
            findings.append(
                TodoFinding(
                    file_path=file_path,
                    line_number=line_number,
                    tag=match.group(1).upper(),
                    text=match.group(2).strip()[:200],
                )
            )
    return findings
