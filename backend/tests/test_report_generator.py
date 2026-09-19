import json
import os
import tempfile

from app.services.report_generator import generate_csv_report, generate_html_report, generate_json_report

SAMPLE_SUMMARY = {
    "total_files": 10,
    "total_dirs": 2,
    "total_loc": 500,
    "languages": {"Python": 400, "Markdown": 100},
    "language_file_counts": {"Python": 8, "Markdown": 2},
    "dependencies": {"requirements.txt": "pip"},
    "large_files": [],
    "todo_count": 3,
    "todos": [],
    "secret_count": 0,
    "secrets": [],
    "average_complexity_score": 12.5,
    "most_complex_files": [],
}


def test_generate_json_report():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "report.json")
        generate_json_report(SAMPLE_SUMMARY, path)
        with open(path) as f:
            data = json.load(f)
        assert data["summary"]["total_files"] == 10


def test_generate_csv_report():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "report.csv")
        generate_csv_report(SAMPLE_SUMMARY, path)
        with open(path) as f:
            content = f.read()
        assert "total_files,10" in content or "total_files" in content


def test_generate_html_report():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "report.html")
        generate_html_report(SAMPLE_SUMMARY, path, "Projeto Teste")
        with open(path) as f:
            content = f.read()
        assert "Projeto Teste" in content
        assert "Python" in content
