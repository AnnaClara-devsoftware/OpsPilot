"""Lightweight cyclomatic-complexity-style estimator.

This is a heuristic (keyword counting), not a full AST-based analyzer for every
language, so it works uniformly across languages without per-language parsers.
It counts branching keywords per file as a proxy for complexity.
"""
import re
from dataclasses import dataclass

BRANCH_KEYWORDS = re.compile(
    r"\b(if|elif|else if|for|while|case|switch|catch|except|and|or|&&|\|\|)\b"
)


@dataclass
class ComplexityResult:
    file_path: str
    branch_points: int
    lines_of_code: int
    complexity_score: float  # branch_points per 100 LOC, rough density metric


def analyze_complexity(file_path: str, content: str) -> ComplexityResult:
    lines = [l for l in content.splitlines() if l.strip()]
    loc = len(lines)
    branch_points = len(BRANCH_KEYWORDS.findall(content))
    score = round((branch_points / loc) * 100, 2) if loc else 0.0
    return ComplexityResult(file_path=file_path, branch_points=branch_points, lines_of_code=loc, complexity_score=score)
