"""
Safe extraction helpers for tar and zip archives to prevent path traversal.
"""
from __future__ import annotations

import os
import tarfile
import zipfile


def safe_tar_extract(tf: tarfile.TarFile, base_dir: str) -> None:
    base = os.path.realpath(base_dir)
    for member in tf.getmembers():
        member_path = os.path.realpath(os.path.join(base, member.name))
        if not member_path.startswith(base + os.sep) and member_path != base:
            raise RuntimeError(f"Entrada insegura no tar: {member.name}")
    tf.extractall(base)


def safe_zip_extract(zf: zipfile.ZipFile, base_dir: str) -> None:
    base = os.path.realpath(base_dir)
    for zi in zf.infolist():
        name = zi.filename
        # reject absolute paths or Windows drive letters
        if os.path.isabs(name) or (len(name) > 1 and name[1] == ':'):
            raise RuntimeError(f"Entrada insegura no zip (absoluta): {name}")
        dest = os.path.realpath(os.path.join(base, name))
        if not dest.startswith(base + os.sep) and dest != base:
            raise RuntimeError(f"Entrada insegura no zip: {name}")
    # after validation, extract members
    for zi in zf.infolist():
        dest = os.path.realpath(os.path.join(base, zi.filename))
        if zi.is_dir() or zi.filename.endswith('/'):
            os.makedirs(dest, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with zf.open(zi, 'r') as src, open(dest, 'wb') as out:
            out.write(src.read())
