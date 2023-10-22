#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python bindings for 7-zip: PROPVARIANT
"""

from datetime import UTC, datetime, timedelta
from enum import IntEnum
from typing import Tuple, Union
from uuid import UUID

from cffi.api import FFI

from . import ffi, lib


class VARTYPE(IntEnum):
    """
    PROPVARIANT type tag
    """

    VT_EMPTY = 0
    VT_NULL = 1
    VT_I2 = 2
    VT_I4 = 3
    VT_R4 = 4
    VT_R8 = 5
    VT_CY = 6
    VT_DATE = 7
    VT_BSTR = 8
    VT_DISPATCH = 9
    VT_ERROR = 10
    VT_BOOL = 11
    VT_VARIANT = 12
    VT_UNKNOWN = 13
    VT_DECIMAL = 14

    VT_I1 = 16
    VT_UI1 = 17
    VT_UI2 = 18
    VT_UI4 = 19
    VT_I8 = 20
    VT_UI8 = 21
    VT_INT = 22
    VT_UINT = 23
    VT_VOID = 24
    VT_HRESULT = 25
    VT_FILETIME = 64


class PropVariant:
    """
    Wrapped PROPVARIANT structure.
    """

    def __init__(self) -> None:
        self.cdata: ffi.CData = ffi.gc(lib.CreatePropVariant(), lib.DeletePropVariant)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<{self.cdata!r}; contains {self.vartype.name}>"

    @property
    def vartype(self) -> VARTYPE:
        """
        Get the type of the PropVariant contents.
        """
        return VARTYPE(self.cdata.vt)  # type: ignore

    @property
    def has_value(self) -> bool:
        """
        Check if the PROPVARIANT contains a value.
        """
        return self.cdata.vt != VARTYPE.VT_EMPTY

    def as_int(self) -> int:
        """
        Get the packed integer.
        """
        vt = self.cdata.vt
        if vt == VARTYPE.VT_I1:
            return int(self.cdata.cVal)  # type: ignore
        if vt == VARTYPE.VT_I2:
            return int(self.cdata.iVal)  # type: ignore
        if vt == VARTYPE.VT_I4:
            return int(self.cdata.lVal)  # type: ignore
        if vt == VARTYPE.VT_I8:
            return int(self.cdata.hVal.QuadPart)  # type: ignore
        if vt == VARTYPE.VT_INT:
            return int(self.cdata.intVal)  # type: ignore
        if vt == VARTYPE.VT_UI1:
            return int(self.cdata.bVal)  # type: ignore
        if vt == VARTYPE.VT_UI2:
            return int(self.cdata.uiVal)  # type: ignore
        if vt == VARTYPE.VT_UI4:
            return int(self.cdata.ulVal)  # type: ignore
        if vt == VARTYPE.VT_UI8:
            return int(self.cdata.uhVal.QuadPart)  # type: ignore
        if vt == VARTYPE.VT_UINT:
            return int(self.cdata.uintVal)  # type: ignore
        raise TypeError(f"Not an integer: {vt}.")

    def as_bool(self) -> bool:
        """
        Get the packed booleean.
        """
        vt = self.cdata.vt
        if vt == VARTYPE.VT_BOOL:
            return bool(self.cdata.boolVal)  # type: ignore
        raise TypeError(f"Not a boolean: {vt}.")

    def as_string(self) -> str:
        """
        Get the packed string.
        """
        vt = self.cdata.vt
        if vt != VARTYPE.VT_BSTR:
            raise TypeError(f"Not a string: {vt}.")
        result = ffi.string(self.cdata.bstrVal)  # type:ignore
        assert isinstance(result, str)
        return result

    def as_bytes(self) -> bytes:
        """
        Get the packed bytestring.
        """
        vt = self.cdata.vt
        if vt != VARTYPE.VT_BSTR:
            raise TypeError(f"Not a bytestring: {vt}.")
        result = ffi.string(ffi.cast("const uint8_t *", self.cdata.bstrVal))  # type: ignore
        assert isinstance(result, bytes)
        return result

    def as_multi_bytes(self) -> Tuple[bytes, ...]:
        """
        Get the packed byte string array.
        """
        vt = self.cdata.vt
        if vt != VARTYPE.VT_BSTR:
            raise TypeError(f"Not a packed byte string array: {vt}.")
        array = ffi.cast("const uint8_t *", self.cdata.bstrVal)  # type: ignore

        offset = 0
        chunks = []
        while size := array[offset]:
            next_offset = offset + 1 + size
            chunks.append(bytes(array[offset + 1 : next_offset]))
            offset = next_offset
        return tuple(chunks)

    def as_uuid(self) -> UUID:
        """
        Get the packed UUID.
        """
        vt = self.cdata.vt
        if vt != VARTYPE.VT_BSTR:
            raise TypeError(f"Not a UUID: {vt}.")
        return UUID(bytes_le=ffi.buffer(self.cdata.bstrVal, 16)[:])  # type: ignore

    def as_datetime(self) -> datetime:
        """
        Get the packed datetime.
        """
        vt = self.cdata.vt
        if vt == VARTYPE.VT_DATE:
            return datetime(1899, 12, 31) + timedelta(days=float(self.cdata.dblVal))
        if vt == VARTYPE.VT_FILETIME:
            return datetime(1601, 1, 1, tzinfo=UTC) + timedelta(microseconds=int(self.cdata.uhVal.QuadPart * 100))
        raise TypeError(f"Not a packed datetime: {vt}.")

    def as_any(self) -> Union[None, bool, int, datetime, str]:
        vt = self.cdata.vt
        if vt in (VARTYPE.VT_EMPTY, VARTYPE.VT_NULL):
            return None
        if vt == VARTYPE.VT_BOOL:
            return bool(self.cdata.boolVal)  # type: ignore
        if vt == VARTYPE.VT_I1:
            return int(self.cdata.cVal)  # type: ignore
        if vt == VARTYPE.VT_I2:
            return int(self.cdata.iVal)  # type: ignore
        if vt == VARTYPE.VT_I4:
            return int(self.cdata.lVal)  # type: ignore
        if vt == VARTYPE.VT_I8:
            return int(self.cdata.hVal.QuadPart)  # type: ignore
        if vt == VARTYPE.VT_INT:
            return int(self.cdata.intVal)  # type: ignore
        if vt == VARTYPE.VT_UI1:
            return int(self.cdata.bVal)  # type: ignore
        if vt == VARTYPE.VT_UI2:
            return int(self.cdata.uiVal)  # type: ignore
        if vt == VARTYPE.VT_UI4:
            return int(self.cdata.ulVal)  # type: ignore
        if vt == VARTYPE.VT_UI8:
            return int(self.cdata.uhVal.QuadPart)  # type: ignore
        if vt == VARTYPE.VT_UINT:
            return int(self.cdata.uintVal)  # type: ignore
        if vt == VARTYPE.VT_BSTR:
            strval = ffi.string(self.cdata.bstrVal)  # type:ignore
            assert isinstance(strval, str)
            return strval
        if vt == VARTYPE.VT_DATE:
            return datetime(1899, 12, 31) + timedelta(days=float(self.cdata.dblVal))
        if vt == VARTYPE.VT_FILETIME:
            return datetime(1601, 1, 1, tzinfo=UTC) + timedelta(microseconds=int(self.cdata.uhVal.QuadPart * 100))
        raise TypeError(f"Unknown or unhandled VARTYPE: {vt}")
