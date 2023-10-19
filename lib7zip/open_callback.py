# -*- coding: utf-8 -*-
from . import ffi, log
from .comtypes import IID_IUnknown
from .py7ziptypes import (
    IID_IArchiveOpenCallback,
    IID_IArchiveOpenSetSubArchiveName,
    IID_IArchiveOpenVolumeCallback,
    IID_ICryptoGetTextPassword,
)
from .simplecom import IUnknownImpl
from .winhelpers import guidp2uuid
from .wintypes import HRESULT, VARTYPE


class ArchiveOpenCallback(IUnknownImpl):
    GUIDS = {
        IID_ICryptoGetTextPassword: "ICryptoGetTextPassword",
        IID_IArchiveOpenCallback: "IArchiveOpenCallback",
        IID_IArchiveOpenVolumeCallback: "IArchiveOpenVolumeCallback",
        IID_IArchiveOpenSetSubArchiveName: "IArchiveOpenSetSubArchiveName",
    }

    def __init__(self, password=None, stream=None):
        if password is None:
            password = ""

            self.password = ffi.new("wchar_t[]", password)

        self.stream = stream
        self.subarchive_name = None

        super().__init__()

    def SetTotal(self, me, files, bytes):
        log.debug("on_set_total")
        return HRESULT.S_OK.value

    def SetCompleted(self, me, files, bytes):
        log.debug("on_set_completed")
        return HRESULT.S_OK.value

    def CryptoGetTextPassword(self, me, password):
        log.debug("GetPassword")
        password[0] = self.password
        return HRESULT.S_OK.value

    def GetProperty(self, me, propID, value):
        log.debug("GetProperty propID={}".format(propID))
        value.vt = VARTYPE.VT_EMPTY
        return HRESULT.S_OK.value

    def GetStream(self, me, name, inStream):
        log.debug("GetStream name={}".format(name))
        return HRESULT.E_NOTIMPL.value

    def SetSubArchiveName(self, me, name):
        log.debug("SetSubArchiveName: {}".format(name))
        # name = ffi.string(name)
        # self.subarchive_name = name
        return HRESULT.E_NOTIMPL.value
