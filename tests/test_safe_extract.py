import io
import os
import tarfile
import zipfile
import tempfile
import pytest

from utils_safe_extract import safe_tar_extract, safe_zip_extract


def test_safe_tar_extract_blocks_traversal(tmp_path):
    # create a tar with a member that tries to escape
    data = io.BytesIO()
    with tarfile.open(fileobj=data, mode='w:xz') as tf:
        ti = tarfile.TarInfo(name='ok/file.txt')
        payload = b'hello'
        ti.size = len(payload)
        tf.addfile(ti, io.BytesIO(payload))
        bad = tarfile.TarInfo(name='../../evil.txt')
        bad.size = len(payload)
        tf.addfile(bad, io.BytesIO(payload))
    data.seek(0)

    with tarfile.open(fileobj=io.BytesIO(data.read()), mode='r:xz') as tf:
        with pytest.raises(RuntimeError):
            safe_tar_extract(tf, str(tmp_path))


def test_safe_zip_extract_blocks_traversal(tmp_path):
    # create a zip with a traversal
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        z.writestr('ok/file.txt', 'hello')
        z.writestr('../../evil.txt', 'hello')
    data.seek(0)

    with zipfile.ZipFile(io.BytesIO(data.read()), mode='r') as z:
        with pytest.raises(RuntimeError):
            safe_zip_extract(z, str(tmp_path))


def test_safe_zip_extract_ok(tmp_path):
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        z.writestr('dir/a.txt', 'x')
    data.seek(0)
    with zipfile.ZipFile(io.BytesIO(data.read()), mode='r') as z:
        safe_zip_extract(z, str(tmp_path))
    assert (tmp_path / 'dir' / 'a.txt').exists()
