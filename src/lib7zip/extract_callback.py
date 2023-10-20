#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from .ffi7z import (
    HRESULT,
    AskMode,
    IID_IArchiveExtractCallback,
    IID_ICompressProgressInfo,
    IID_ICryptoGetTextPassword,
    IID_ICryptoGetTextPassword2,
    IID_ISequentialOutStream,
    IUnknownImpl,
    ffi,
)
from .stream import FileOutStream, SimpleOutStream


class ArchiveExtractCallback(IUnknownImpl):
    """Base class for extract callbacks."""

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
        return HRESULT.S_OK.value

    def SetCompleted(self, complete_value):
        return HRESULT.S_OK.value

    def SetRatioInfo(self, in_size, out_size):
        return HRESULT.S_OK.value

    def GetStream(self, index, out_stream, ask_extract_mode):
        raise NotImplementedError()

    def PrepareOperation(self, ask_extract_mode):
        return HRESULT.S_OK.value

    def SetOperationResult(self, operation_result):
        return HRESULT.S_OK.value

    def CryptoGetTextPassword(self, password):
        password[0] = password_buf
        return HRESULT.S_OK.value

    def CryptoGetTextPassword2(self, has_password, password):
        has_password[0] = password is not None
        password[0] = password_buf
        return HRESULT.S_OK.value


class ArchiveExtractToDirectoryCallback(ArchiveExtractCallback):
    """Archive extract callback that unpacks each item into a target directory."""

    def __init__(self, archive, directory, password):
        self.archive = archive
        self.directory = Path(directory)
        self.streams = {}
        super().__init__(password)

    def GetStream(self, index, out_stream, ask_extract_mode):
        if ask_extract_mode != AskMode.kExtract.value:
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
    def __init__(self, stream, index, password):
        self.stream = SimpleOutStream(stream)
        self.index = index
        super().__init__(password)

    def GetStream(self, index, out_stream, ask_extract_mode):
        if ask_extract_mode != AskMode.kExtract.value:
            return HRESULT.S_OK.value

        if index == self.index:
            out_stream[0] = self.stream.instances[IID_ISequentialOutStream]
            return HRESULT.S_OK.value
        else:
            out_stream[0] = ffi.NULL
            return HRESULT.S_OK.value
