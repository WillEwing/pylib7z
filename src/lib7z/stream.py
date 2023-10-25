#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python bindings for the 7-Zip Library: IO Streams
"""

from os import SEEK_CUR, SEEK_END, SEEK_SET, PathLike
from typing import BinaryIO, Union

from .ffi7z import ffi  # pylint: disable=no-name-in-module
from .hresult import HRESULT
from .iids import (
    IID_IInStream,
    IID_IOutStream,
    IID_ISequentialInStream,
    IID_ISequentialOutStream,
    IID_IStreamGetSize,
)
from .unknown import PyUnknown


class PyInStream(PyUnknown):
    """
    IInStream implemetation backed by a Python binary IO stream.
    """

    # pylint: disable=invalid-name

    IIDS = (
        IID_IInStream,
        IID_ISequentialInStream,
        IID_IStreamGetSize,
    )

    def __init__(self, stream: BinaryIO, stream_size=None) -> None:
        self.stream = stream
        self.stream_size = stream_size
        super().__init__()

    def Read(self, array_ptr, bytes_to_read, bytes_read):
        """Read from the stream."""
        try:
            array_buf = ffi.buffer(array_ptr, bytes_to_read)
            bytes_read[0] = self.stream.readinto(array_buf)
            return HRESULT.S_OK
        except IOError:
            return HRESULT.E_FAIL

    def Seek(self, offset, origin, new_position):
        """Seek to a new position in the stream."""
        try:
            position = self.stream.seek(offset, origin)
            if new_position != ffi.NULL:
                new_position[0] = position
            return HRESULT.S_OK
        except IOError:
            return HRESULT.E_FAIL

    def GetSize(self, size_ptr):
        """Get the size of the backing object."""
        last_position = self.stream.seek(0, SEEK_CUR)
        size_ptr[0] = self.stream.seek(0, SEEK_END)
        self.stream.seek(last_position, SEEK_SET)
        return HRESULT.S_OK


class FileInStream(PyInStream):
    """
    IInStream implemetation backed by a Python file stream.
    """

    def __init__(self, filename: Union[PathLike, str]) -> None:
        super().__init__(open(filename, "rb"))


class PyOutStream(PyUnknown):
    """
    IOutStream implemetation backed by a Python binary IO stream.
    """

    # pylint: disable=invalid-name

    IIDS = (
        IID_IOutStream,
        IID_ISequentialOutStream,
    )

    def __init__(self, stream: BinaryIO) -> None:
        self.stream = stream
        super().__init__()

    def Write(self, array_ptr, bytes_to_write, bytes_written):
        """Write bytes to the stream."""
        try:
            array_buf = ffi.buffer(array_ptr, bytes_to_write)
            bytes_written[0] = self.stream.write(array_buf)
            return HRESULT.S_OK
        except IOError:
            return HRESULT.E_FAIL

    def Seek(self, offset, origin, new_position):
        """Seek to a new position in the stream."""
        try:
            position = self.stream.seek(offset, origin)
            if new_position != ffi.NULL:
                new_position[0] = position
            return HRESULT.S_OK
        except IOError:
            return HRESULT.E_FAIL


class FileOutStream(PyOutStream):
    """
    IOutStream implemetation backed by a Python file stream.
    """

    def __init__(self, filename: Union[PathLike, str]) -> None:
        super().__init__(open(filename, "wb"))

    def Close(self) -> None:
        """Close the stream."""
        self.stream.close()

    def Release(self):
        refs = super().Release()
        if refs == 0:
            self.Close()
        return refs
