#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python bindings for 7-Zip library: format registry.
"""

from collections.abc import Sequence
from enum import IntEnum, IntFlag
from typing import Tuple
from uuid import UUID

from . import ffi, lib
from .propvariant import PropVariant

__all__ = ("FormatFlag", "FormatProp", "FormatInfo")


class FormatFlag(IntFlag):
    """
    Archive format flags
    """

    KEEP_NAME = 1 << 0
    ALT_STREAMS = 1 << 1
    NT_SECURE = 1 << 2
    FIND_SIGNATURE = 1 << 3
    MULTI_SIGNATURE = 1 << 4
    USE_GLOBAL_OFFSET = 1 << 5
    START_OPEN = 1 << 6
    PURE_START_OPEN = 1 << 7
    BACKWARD_OPEN = 1 << 8
    PRE_ARC = 1 << 9
    SYM_LINKS = 1 << 10
    HARD_LINKS = 1 << 11
    BY_EXT_ONLY_OPEN = 1 << 12
    HASH_HANDLER = 1 << 13
    CTIME = 1 << 14
    CTIME_DEFAULT = 1 << 15
    ATIME = 1 << 16
    ATIME_DEFAULT = 1 << 17
    MTIME = 1 << 18
    MTIME_DEFAULT = 1 << 19


class FormatProp(IntEnum):
    """
    Archive format properties
    """

    NAME = 0
    CLASS_ID = 1
    EXTENSION = 2
    ADD_EXTENSION = 3
    UPDATE = 4
    KEEP_NAME = 5
    SIGNATURE = 6
    MULTI_SIGNATURE = 7
    SIGNATURE_OFFSET = 8
    ALT_STREAMS = 9
    NT_SECURE = 10
    FLAGS = 11
    TIME_FLAGS = 12


def _get_num_formats() -> int:
    """
    Get the number of archive formats.
    """
    num_formats_ptr = ffi.new("uint32_t *")
    hresult = lib.GetNumberOfFormats(num_formats_ptr)
    if hresult < 0:
        raise RuntimeError(f"HRESULT: {hresult:#010x}")
    return int(num_formats_ptr[0])


def _get_format_property(index: int, prop_id: int) -> PropVariant:
    """
    Get property `prop_id` of archive format `index`.
    """
    prop_var = PropVariant()
    hresult = lib.GetHandlerProperty2(index, prop_id, prop_var.cdata)  # type: ignore
    if hresult < 0:
        raise RuntimeError(f"HRESULT: {hresult:#010x}")
    return prop_var


class FormatInfo:
    """
    Archive format info.
    """

    def __init__(self, index: int) -> None:
        if not (0 <= index < _get_num_formats()):
            raise IndexError("Format index out of range.")
        self.index = index

    @property
    def name(self) -> str:
        """
        The name of the archive format.
        """
        prop_var = _get_format_property(self.index, FormatProp.NAME.value)
        return prop_var.as_string()

    @property
    def clsid(self) -> UUID:
        """
        The class id of the archive handler.
        """
        prop_var = _get_format_property(self.index, FormatProp.CLASS_ID.value)
        return prop_var.as_uuid()

    @property
    def flags(self) -> FormatFlag:
        """
        Archive format flags.
        """
        prop_var = _get_format_property(self.index, FormatProp.FLAGS.value)
        return FormatFlag(prop_var.as_int())

    @property
    def extensions(self) -> Tuple[str, ...]:
        """
        Common file extensions for the archive type.
        """
        prop_var = _get_format_property(self.index, FormatProp.EXTENSION.value)
        if prop_var.has_value:
            return tuple(prop_var.as_string().split())
        return ()

    @property
    def signatures(self) -> Tuple[bytes, ...]:
        """
        Magic numbers for format detection.
        """
        if FormatFlag.MULTI_SIGNATURE in self.flags:
            prop_var = _get_format_property(self.index, FormatProp.MULTI_SIGNATURE.value)
            if prop_var.has_value:
                return prop_var.as_multi_bytes()
            return ()
        else:
            prop_var = _get_format_property(self.index, FormatProp.SIGNATURE.value)
            if prop_var.has_value:
                return (prop_var.as_bytes(),)
            return ()

    @property
    def signature_offset(self) -> int:
        """
        Expected position of magic numbers in archive files.
        """
        return 0


class FormatRegistry(Sequence[FormatInfo]):
    """
    Read-only access to 7-zip's archive format registry.
    """

    def __len__(self) -> int:
        return _get_num_formats()

    def __getitem__(self, index: int) -> FormatInfo:  # type: ignore
        if isinstance(index, int):
            return FormatInfo(index)


formats = FormatRegistry()
