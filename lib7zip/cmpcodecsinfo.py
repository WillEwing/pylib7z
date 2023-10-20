# -*- coding: utf-8 -*-
import logging

log = logging.getLogger(__name__)

from .ffi7z import *


class CompressCodecsInfo(IUnknownImpl):
    IIDS = {
        IID_ICompressCodecsInfo: "ICompressCodecsInfo",
    }

    def GetNumMethods(self, numMethods):
        return lib.GetNumberOfMethods(numMethods)

    def GetProperty(self, index, propID, value):
        return lib.GetMethodProperty(index, propID, value)

    def CreateDecoder(self, index, iid, coder):
        classid = MarshallGUID(methods[index].decoder)
        return lib.CreateObject(classid, iid, coder)

    def CreateEncoder(self, index, iid, coder):
        classid = MarshallGUID(methods[index].encoder)
        return lib.CreateObject(classid, iid, coder)
