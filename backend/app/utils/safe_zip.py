"""Safe ZIP extraction utilities: guards against path traversal (zip-slip) and zip bombs."""
import os
import zipfile
from pathlib import Path

MAX_UNCOMPRESSED_SIZE = 500 * 1024 * 1024  # 500MB safety cap
MAX_FILE_COUNT = 20000


class UnsafeZipError(Exception):
    pass


def safe_extract(zip_path: str, dest_dir: str) -> str:
    """Extract a ZIP file safely into dest_dir. Returns dest_dir on success."""
    dest = Path(dest_dir).resolve()
    dest.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as zf:
        infos = zf.infolist()
        if len(infos) > MAX_FILE_COUNT:
            raise UnsafeZipError("ZIP contem excesso de arquivos")

        total_size = sum(i.file_size for i in infos)
        if total_size > MAX_UNCOMPRESSED_SIZE:
            raise UnsafeZipError("ZIP excede o tamanho descompactado maximo permitido")

        for info in infos:
            target_path = (dest / info.filename).resolve()
            if not str(target_path).startswith(str(dest)):
                raise UnsafeZipError(f"Caminho suspeito detectado no ZIP: {info.filename}")

        zf.extractall(dest)

    return str(dest)
