import os
import tempfile
import zipfile

import pytest

from app.utils.safe_zip import UnsafeZipError, safe_extract


def test_safe_extract_normal_zip():
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = os.path.join(tmp, "test.zip")
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("hello.txt", "world")

        dest = os.path.join(tmp, "extracted")
        safe_extract(zip_path, dest)
        assert os.path.exists(os.path.join(dest, "hello.txt"))


def test_safe_extract_blocks_path_traversal():
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = os.path.join(tmp, "evil.zip")
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("../../etc/evil.txt", "pwned")

        dest = os.path.join(tmp, "extracted")
        with pytest.raises(UnsafeZipError):
            safe_extract(zip_path, dest)
