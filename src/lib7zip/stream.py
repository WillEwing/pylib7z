#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import BinaryIO

from .ffi7z import (
    HRESULT,
    IID_IInStream,
    IID_IOutStream,
    IID_ISequentialInStream,
    IID_ISequentialOutStream,
    IUnknownImpl,
    ffi,
)


class SimpleInStream(IUnknownImpl):
    """
    Implementation of IInStream wrapping a Python BinaryIO object.
    """

    IIDS = (
        IID_ISequentialInStream,
        IID_IInStream,
    )

    def __init__(self, stream):
        self.stream = stream
        super().__init__()

    def Read(self, data, bytes_to_read, bytes_read_ptr):
        buffer = ffi.buffer(data, bytes_to_read)
        bytes_read = self.stream.readinto(buffer)
        if bytes_read_ptr != ffi.NULL:
            bytes_read_ptr[0] = bytes_read
        return HRESULT.S_OK.value

    def Seek(self, offset, origin, position_ptr):
        position = self.stream.seek(offset, origin)
        if position_ptr != ffi.NULL:
            position_ptr[0] = position
        return HRESULT.S_OK.value


class FileInStream(SimpleInStream):
    """
    Implementation of IInStream against a file on-disk.
    """

    def __init__(self, filename):
        stream = open(filename, "rb")
        super().__init__(stream)


class SimpleOutStream(IUnknownImpl):
    """
    Implementation of IOutStream wrapping a Python BinaryIO object.
    """

    IIDS = (
        IID_ISequentialOutStream,
        IID_IOutStream,
    )

    def __init__(self, stream):
        self.stream = stream
        super().__init__()

    def Write(self, data, bytes_to_write, bytes_written_ptr):
        buffer = ffi.buffer(data, bytes_to_write)
        bytes_written = self.stream.write(buffer)
        if bytes_written_ptr != ffi.NULL:
            bytes_written_ptr[0] = bytes_written
        return HRESULT.S_OK.value

    def Seek(self, offset, origin, position_ptr):
        position = self.stream.seek(offset, origin)
        if position_ptr != ffi.NULL:
            position_ptr[0] = position
        return HRESULT.S_OK.value


class FileOutStream(SimpleOutStream):
    """
    Implementation of IOutStream against a file on-disk.
    """

    def __init__(self, filename):
        stream = open(filename, "wb")
        super().__init__(stream)
