from app.services.complexity_analyzer import analyze_complexity
from app.services.language_detector import detect_language
from app.services.secret_scanner import scan_text_for_secrets
from app.services.todo_scanner import scan_text_for_todos


def test_detect_language():
    assert detect_language("main.py") == "Python"
    assert detect_language("app.tsx") == "TypeScript"
    assert detect_language("unknownfile.xyz") is None


def test_scan_text_for_todos_finds_tags():
    content = "print('hi')\n# TODO: refactor this\n# FIXME broken logic\nnormal line\n"
    findings = scan_text_for_todos("file.py", content)
    tags = {f.tag for f in findings}
    assert "TODO" in tags
    assert "FIXME" in tags
    assert len(findings) == 2


def test_scan_text_for_secrets_detects_aws_key():
    content = 'aws_key = "AKIAABCDEFGHIJKLMNOP"'
    findings = scan_text_for_secrets("config.py", content)
    assert any(f.rule_name == "AWS Access Key" for f in findings)


def test_scan_text_for_secrets_no_false_positive_on_clean_code():
    content = "def add(a, b):\n    return a + b\n"
    findings = scan_text_for_secrets("clean.py", content)
    assert findings == []


def test_analyze_complexity_counts_branches():
    content = "if x:\n    pass\nelif y:\n    pass\nfor i in range(10):\n    pass\n"
    result = analyze_complexity("f.py", content)
    assert result.branch_points >= 3
    assert result.lines_of_code == 6
