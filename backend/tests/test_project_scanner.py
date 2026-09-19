import os
import tempfile

from app.services.project_scanner import scan_project


def test_scan_project_end_to_end():
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "main.py"), "w") as f:
            f.write("def main():\n    # TODO: implement\n    if True:\n        pass\n")
        with open(os.path.join(tmp, "requirements.txt"), "w") as f:
            f.write("fastapi==0.115.6\n")
        with open(os.path.join(tmp, "secrets.py"), "w") as f:
            f.write('api_key = "AKIAABCDEFGHIJKLMNOP"\n')

        result = scan_project(tmp)
        summary = result.to_summary_dict()

        assert summary["total_files"] == 3
        assert summary["total_loc"] > 0
        assert "Python" in summary["languages"]
        assert summary["todo_count"] == 1
        # The sample secret matches more than one heuristic rule (AWS key +
        # generic API key pattern), which is expected: overlapping detections
        # are safer than missed ones for a security scanner.
        assert summary["secret_count"] >= 1
        assert "requirements.txt" in summary["dependencies"]


def test_scan_project_ignores_common_dirs():
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "node_modules"))
        with open(os.path.join(tmp, "node_modules", "lib.js"), "w") as f:
            f.write("console.log('should be ignored')\n")
        with open(os.path.join(tmp, "index.js"), "w") as f:
            f.write("console.log('hello')\n")

        result = scan_project(tmp)
        summary = result.to_summary_dict()
        assert summary["total_files"] == 1
