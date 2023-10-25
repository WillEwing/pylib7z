#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python bindings for the 7-Zip Library: archive extract callbacks
"""

from enum import IntEnum
from logging import getLogger
from pathlib import Path
from typing import Optional

from .ffi7zip import ffi, lib  # pylint: disable=no-name-in-module
from .hresult import HRESULT
from .iids import (
    IID_IArchiveExtractCallback,
    IID_IArchiveExtractCallbackMessage2,
    IID_ICompressProgressInfo,
    IID_ICryptoGetTextPassword,
    IID_ICryptoGetTextPassword2,
    IID_ISequentialOutStream,
)
from .stream import FileOutStream, PyOutStream
from .unknown import PyUnknown

log = getLogger("lib7zip")


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
        IID_IArchiveExtractCallbackMessage2,
    )

    def __init__(self, password):
        self.last_op_result = None
        self.password = password
        super().__init__()

    def ReportExtractResult(self, index_type, index, op_res):
        return HRESULT.S_OK

    def SetTotal(self, total):
        return HRESULT.S_OK

    def SetCompleted(self, complete_value):
        return HRESULT.S_OK

    def SetRatioInfo(self, in_size, out_size):
        return HRESULT.S_OK

    def SetOperationResult(self, op_result):
        self.last_op_result = op_result
        return HRESULT.S_OK

    def GetStream(self, index, out_stream, ask_extract_mode):
        return HRESULT.E_NOTIMPL

    def PrepareOperation(self, ask_extract_mode):
        return HRESULT.S_OK

    def CryptoGetTextPassword(self, password):
        if self.password:
            password[0] = lib.SysAllocStringLen(self.password, len(self.password))
        else:
            password[0] = ffi.NULL
        return HRESULT.S_OK

    def CryptoGetTextPassword2(self, has_password, password):
        if has_password != ffi.NULL:
            has_password[0] = self.password is not None
        if password != ffi.NULL:
            if self.password:
                password[0] = lib.SysAllocStringLen(self.password, len(self.password))
            else:
                password[0] = ffi.NULL
        return HRESULT.S_OK

    def cleanup(self):
        raise NotImplementedError()


class ArchiveExtractToDirectoryCallback(ArchiveExtractCallback):
    """Archive extract callback that unpacks into a directory."""

    # pylint: disable=invalid-name

    def __init__(self, archive, directory, password, *, strip_components=0):
        self.archive = archive
        self.directory = Path(directory)
        self._out_stream: Optional[FileOutStream] = None
        self.strip_components = strip_components
        super().__init__(password)

    def GetStream(self, index, out_stream, ask_extract_mode):
        if self._out_stream is not None:
            if self._out_stream.refs != 0:
                log.warning("ExtractCallback._out_stream: refs != 0")
            self._out_stream = None

        if ask_extract_mode != AskMode.EXTRACT:
            return HRESULT.S_OK.value

        item = self.archive[index]
        path = Path(item.path)

        if len(path.parts) < self.strip_components:
            out_stream[0] = ffi.NULL
            return HRESULT.S_OK

        path = self.directory / Path(*path.parts[self.strip_components :])
        if self.directory not in (path, *path.parents):
            out_stream[0] = ffi.NULL
            return HRESULT.S_FALSE

        if item.is_dir:
            path.mkdir(exist_ok=True, parents=True)
            out_stream[0] = ffi.NULL
        else:
            path.parent.mkdir(exist_ok=True, parents=True)
            self._out_stream = FileOutStream(path)
            out_stream[0] = self._out_stream.get_instance(IID_ISequentialOutStream)

        return HRESULT.S_OK

    def cleanup(self):
        pass


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
            out_stream[0] = self.stream.get_instance(IID_ISequentialOutStream)
            return HRESULT.S_OK.value
        else:
            out_stream[0] = ffi.NULL
            return HRESULT.S_OK.value

    def cleanup(self):
        self.stream.stream.flush()
