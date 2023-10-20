#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .ffi7z import *


class ArchiveOpenCallback(IUnknownImpl):
    """
    Archive open callback implementation.
    """

    IIDS = (
        IID_ICryptoGetTextPassword,
        IID_IArchiveOpenCallback,
        IID_IArchiveOpenVolumeCallback,
        IID_IArchiveOpenSetSubArchiveName,
    )

    def __init__(self, password=None, stream=None):
        self.password = password
        self.password_buf = ffi.new("wchar_t[]", password) if password else ffi.NULL
        self.stream = stream
        self.subarchive_name = None
        super().__init__()

    def SetTotal(self, files, bytes):
        return HRESULT.S_OK.value

    def SetCompleted(self, files, bytes):
        return HRESULT.S_OK.value

    def CryptoGetTextPassword(self, password_ptr):
        password[0] = self.password_buf
        return RESULT.S_OK.value

    def GetProperty(self, prop_id, value):
        value.vt = VARTYPE.VT_EMPTY
        return HRESULT.S_OK.value

    def GetStream(self, name, in_stream):
        return HRESULT.E_NOTIMPL.value

    def SetSubArchiveName(self, name):
        return HRESULT.E_NOTIMPL.value
