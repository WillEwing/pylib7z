# -*- coding: utf-8 -*-
import logging
import os
import sys
from collections import namedtuple
from typing import Generator
from zipfile import ZipFile

import pytest

from lib7z import Archive
from lib7z.archive import ExtractError

log = logging.getLogger("lib7z")

SIMPLE_ARCHIVES = ("tests/simple.7z", "tests/simple.zip")


ArchiveItemEx = namedtuple("ArchiveItemEx", ("is_dir", "crc", "contents"))


def IX(is_dir=False, crc=None, contents=""):  # pylint: disable=invalid-name
    "Shortcut function to pack _IX tuples."
    return ArchiveItemEx(is_dir, crc, contents)


J = os.path.join

COMPLEX_MD = {
    J("complex", "articles"): IX(True),
    J("complex", "articles", "the definate article.txt"): IX(False, 0x3C456DE6, "the"),
    J("complex", "articles", "the indefinate article.txt"): IX(False, 0xE8B7BE43, "a"),
    J("complex", "goodbye.txt"): IX(False, 0x3078A778, "Goodbye!"),
    J("complex", "hello.txt"): IX(False, 0x9D2ACC56, "Hello!"),
    # J('complex','unicode.txt'): IX(False, 0x226F311C, 'Úñï¢ðÐê †ê§†!'),
    J("complex", "empty.txt"): IX(False, None, ""),
    J("complex", "empty"): IX(True),
    J("complex"): IX(True),
}


def test_complex():
    """
    Complex archive metadata and files can be read.
    """
    log.debug("test_complex()")
    with Archive("tests/complex.7z") as archive:
        for item in archive:
            log.debug(item.path)
            try:
                md = COMPLEX_MD[item.path]
            except KeyError as ex:
                log.warning("key %s not present", ex.args[0])
                continue

            assert item.is_dir == md.is_dir
            if md.crc is None:
                assert item.crc is None
            else:
                assert item.crc == md.crc

            if not item.is_dir:
                assert item.read_text() == md.contents
        logging.debug("done iterating archives")


def test_extract_dir_complex(tmpdir):
    """
    Complex archives can be extracted to a directory.
    """
    with Archive("tests/complex.7z") as archive:
        archive.extract(tmpdir)

    for path, md in COMPLEX_MD.items():
        if md.contents:
            with open(os.path.join(tmpdir, path), encoding="utf-8") as f:
                file_contents = f.read()
                # if 'unicode' in path:
                # 	import pdb; pdb.set_trace()
                assert file_contents == md.contents


@pytest.mark.parametrize("path", SIMPLE_ARCHIVES)
def test_extract_stream(path):
    """
    Files can be extracted to a stream.
    """
    with Archive(path) as archive:
        assert archive[0].read_text() == "Hello World!\n"


@pytest.mark.parametrize("path", SIMPLE_ARCHIVES)
def test_extract_dir(path, tmpdir):
    """
    Files can be extracted to a directory.
    """
    with Archive(path) as archive:
        archive.extract(tmpdir)

    with open(os.path.join(tmpdir, "hello.txt"), "rb") as f:
        assert f.read() == b"Hello World!\n"


def test_extract_with_pass():
    """
    Files can be extracted with a password.
    """
    with Archive("tests/simple_crypt.7z") as archive:
        assert archive[0].path == "hello.txt"
        assert archive[0].read_text(password="password") == "Hello World!\n"


def test_extract_with_pass_dir(tmpdir):
    """
    Files can be extracted to a directory with a password.
    """
    with Archive("tests/simple_crypt.7z", password="password") as archive:
        archive.extract(tmpdir)

    with open(os.path.join(tmpdir, "hello.txt"), "rb") as f:
        assert f.read() == b"Hello World!\n"


@pytest.mark.xfail(raises=ExtractError)
def test_extract_badpass():
    """
    Files can't be extracted with a wrong password.
    """
    with Archive("tests/simple_crypt.7z") as archive:
        assert archive[0].read_bytes(password="notthepass") == b"Hello World!\n"


def test_extract_extract_many_files_to_dir(tmpdir):
    """
    Test extracting large numbers of files to a directory.
    If extract() does not close file handles during its process, this will fail.
    """

    temp_zip_path = os.path.join(tmpdir, "many_files.zip")
    with ZipFile(temp_zip_path, "w") as temp_zip:
        # NOTE: Default file limit on Windows is 512.
        for index in range(65536):
            temp_zip.writestr(f"file-{index}", f"This is file {index}.")

    with Archive(temp_zip_path) as archive:
        archive.extract(tmpdir)
