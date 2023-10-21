#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python bindings for the 7-Zip Library: archive extract callbacks
"""

from enum import IntEnum
from pathlib import Path

from .ffi7zip import ffi  # pylint: disable=no-name-in-module
from .hresult import HRESULT
from .iids import (
    IID_IArchiveExtractCallback,
    IID_ICompressProgressInfo,
    IID_ICryptoGetTextPassword,
    IID_ICryptoGetTextPassword2,
    IID_ISequentialOutStream,
)
from .stream import FileOutStream, PyOutStream
from .unknown import PyUnknown


class AskMode(IntEnum):
    """
    Values for the ask_extract_mode argument in GetStream.
    """

    EXTRACT = 0
    TEST = 1
    SKIP = 2


class OperationResult(IntEnum):
    """
    Values for the op_result argument in SetOperationResult.
    """

    OK = 0
    UNSUPPORTED_METHOD = 1
    DATA_ERROR = 2
    CRC_ERROR = 3


class ArchiveExtractCallback(PyUnknown):
    """Base class for archive extract callbacks."""

    # pylint: disable=invalid-name

    IIDS = (
        IID_IArchiveExtractCallback,
        IID_ICryptoGetTextPassword,
        IID_ICryptoGetTextPassword2,
        IID_ICompressProgressInfo,
    )

    def __init__(self, password):
        self.password = password
        self.password_buf = ffi.new("wchar_t[]", password) if password else ffi.NULL
        super().__init__()

    def SetTotal(self, total):
        return HRESULT.S_OK

    def SetCompleted(self, complete_value):
        return HRESULT.S_OK

    def SetRatioInfo(self, in_size, out_size):
        return HRESULT.S_OK

    def SetOperationResult(self, op_result):
        return HRESULT.S_OK

    def GetStream(self, index, out_stream, ask_extract_mode):
        return HRESULT.E_NOTIMPL

    def PrepareOperation(self, ask_extract_mode):
        return HRESULT.S_OK

    def CryptoGetTextPassword(self, password):
        password[0] = self.password_buf

    def CryptoGetTextPassword2(self, has_password, password):
        has_password[0] = self.password is not None
        password[0] = self.password_buf


class ArchiveExtractToDirectoryCallback(ArchiveExtractCallback):
    """Archive extract callback that unpacks into a directory."""

    # pylint: disable=invalid-name

    def __init__(self, archive, directory, password):
        self.archive = archive
        self.directory = Path(directory)
        self.streams = {}
        super().__init__(password)

    def GetStream(self, index, out_stream, ask_extract_mode):
        if ask_extract_mode != AskMode.EXTRACT:
            return HRESULT.S_OK.value

        if index in self.streams:
            return self.streams[index]

        item = self.archive[index]

        path = self.directory / item.path
        if not self.directory in (path, *path.parents):
            return HRESULT.S_FALSE.value

        if item.is_dir:
            path.mkdir(exist_ok=True, parents=True)
            out_stream[0] = ffi.NULL
        else:
            self.streams[index] = stream = FileOutStream(path)
            out_stream[0] = stream.instances[IID_ISequentialOutStream]

        return HRESULT.S_OK.value


class ArchiveExtractToStreamCallback(ArchiveExtractCallback):
    """Archive extract callback that unpacks everything into one stream."""

    # pylint: disable=invalid-name

    def __init__(self, stream, index, password):
        self.stream = PyOutStream(stream)
        self.index = index
        super().__init__(password)

    def GetStream(self, index, out_stream, ask_extract_mode):
        if ask_extract_mode != AskMode.EXTRACT:
            return HRESULT.S_OK.value

        if index == self.index:
            out_stream[0] = self.stream.instances[IID_ISequentialOutStream]
            return HRESULT.S_OK.value
        else:
            out_stream[0] = ffi.NULL
            return HRESULT.S_OK.value
