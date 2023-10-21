#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python bindings for the 7-Zip Library: ArchiveOpenCallbacks
"""

from .ffi7zip import ffi  # pylint: disable=no-name-in-module
from .hresult import HRESULT
from .iids import (
    IID_IArchiveOpenCallback,
    IID_IArchiveOpenSetSubArchiveName,
    IID_IArchiveOpenVolumeCallback,
    IID_ICryptoGetTextPassword,
)
from .propvariant import VARTYPE
from .unknown import PyUnknown


class ArchiveOpenCallback(PyUnknown):
    """
    Archive Open Callbacks
    """

    # pylint: disable=invalid-name

    IIDS = (
        IID_ICryptoGetTextPassword,
        IID_IArchiveOpenCallback,
        IID_IArchiveOpenVolumeCallback,
        IID_IArchiveOpenSetSubArchiveName,
    )

    def __int__(self, password=None, stream=None):
        self.password = password
        self.password_buf = ffi.new("wchar_t []", password) if password else ffi.NULL
        self.stream = stream
        self.subarchive_name = None
        super().__init__()

    def SetTotal(self, files, bytes):
        return HRESULT.S_OK

    def SetCompleted(self, files, bytes):
        return HRESULT.S_OK

    def CryptoGetTextPassword(self, password_ptr):
        password_ptr[0] = self.password_buf
        return HRESULT.S_OK

    def GetProperty(self, prop_id, value):
        value.vt = VARTYPE.VT_EMPTY
        return HRESULT.S_OK

    def GetStream(self, name, in_stream):
        return HRESULT.E_NOTIMPL

    def SetSubArchiveName(self, name):
        return HRESULT.E_NOTIMPL
