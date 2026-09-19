"""Generates HTML, JSON and CSV reports from an analysis summary dict."""
import csv
import io
import json
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATES_DIR = Path(__file__).parent / "templates"

_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html"]),
)


def generate_json_report(summary: dict, output_path: str) -> str:
    payload = {"generated_at": datetime.now(timezone.utc).isoformat(), "summary": summary}
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    return output_path


def generate_csv_report(summary: dict, output_path: str) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["metric", "value"])
    writer.writerow(["total_files", summary.get("total_files", 0)])
    writer.writerow(["total_dirs", summary.get("total_dirs", 0)])
    writer.writerow(["total_loc", summary.get("total_loc", 0)])
    writer.writerow(["todo_count", summary.get("todo_count", 0)])
    writer.writerow(["secret_count", summary.get("secret_count", 0)])
    writer.writerow(["average_complexity_score", summary.get("average_complexity_score", 0)])
    writer.writerow([])
    writer.writerow(["language", "loc", "file_count"])
    for lang, loc in summary.get("languages", {}).items():
        count = summary.get("language_file_counts", {}).get(lang, 0)
        writer.writerow([lang, loc, count])

    with open(output_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buffer.getvalue())
    return output_path


def generate_html_report(summary: dict, output_path: str, project_name: str) -> str:
    template = _env.get_template("report.html.j2")
    html = template.render(
        summary=summary,
        project_name=project_name,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return output_path
