#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for lib7zip.formats
"""

import pytest

import lib7zip.format_registry

pytestmark = pytest.mark.skipif(
    lib7zip.format_registry._get_num_formats() == 0,  # pylint: disable=protected-access
    reason="FFI reports no supported archive formats",
)


@pytest.mark.xfail(raises=IndexError)
def test_low_index():
    """
    FormatInfo can't be constrcuted with negative index.
    """
    _ = lib7zip.format_registry.FormatInfo(-1)


@pytest.mark.xfail(raises=IndexError)
def test_high_index():
    """
    FormatInfo can't be constructed with out-of-range index.
    """
    num_formats = lib7zip.format_registry._get_num_formats()  # pylint: disable=protected-access
    _ = lib7zip.format_registry.FormatInfo(num_formats + 1)


def test_first_format_name():
    """
    Lowest-indexed name is readable.
    """
    fmt = lib7zip.format_registry.FormatInfo(0)
    assert fmt.name


def test_last_format_name():
    """
    Highest-indexed name is readable.
    """
    last_idx = lib7zip.format_registry._get_num_formats() - 1  # pylint: disable=protected-access
    fmt = lib7zip.format_registry.FormatInfo(last_idx)
    assert fmt.name


def test_iterate_formats():
    """
    Formats can be iterated over.
    """
    for fmt in lib7zip.format_registry.formats:
        assert fmt.name


def test_fmt_extensions():
    """
    Format file extensions list is readable.
    """
    fmt = lib7zip.format_registry.formats[0].extensions
    assert fmt


def test_format_no_signature():
    """
    Lack of signatures is readable.
    """
    for fmt in lib7zip.format_registry.formats:
        if fmt.name == "IHex":
            assert fmt.signatures == ()
            break


def test_format_signature():
    """
    Single signatures are readable.
    """
    for fmt in lib7zip.format_registry.formats:
        if lib7zip.format_registry.FormatFlag.MULTI_SIGNATURE not in fmt.flags:
            if fmt.signatures != ():
                assert True
                return

    assert False


def test_format_multi_signature():
    """
    Multiple signatures are readable.
    """
    for fmt in lib7zip.format_registry.formats:
        if lib7zip.format_registry.FormatFlag.MULTI_SIGNATURE in fmt.flags:
            assert fmt.signatures
            return

    pytest.skip(msg="No multi-signature formats found in registry.")
