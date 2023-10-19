# -*- coding: utf-8 -*-
import logging
from os import PathLike
from typing import BinaryIO

from . import ffi, wintypes
from .py7ziptypes import (
    IID_IInStream,
    IID_IOutStream,
    IID_ISequentialInStream,
    IID_ISequentialOutStream,
)
from .simplecom import IUnknownImpl
from .winhelpers import guidp2uuid
from .wintypes import HRESULT

log = logging.getLogger(__name__)


class FileInStream(IUnknownImpl):
    """
    Implementation of IInStream and ISequentialInStream on top of python file-like objects

    Creator responsible for closing the file-like objects.
    """

    GUIDS = {
        IID_IInStream: "IInStream",
        IID_ISequentialInStream: "ISequentialInStream",
    }

    def __init__(self, file: BinaryIO | PathLike | str) -> None:
        if isinstance(file, (PathLike, str)):
            self.filelike: BinaryIO = open(file, "rb")
        else:
            self.filelike = file
        super().__init__()

    def Read(self, me, data, size, processed_size):
        log.debug("Read size=%d", size)
        buf = self.filelike.read(size)
        psize = len(buf)

        if processed_size != ffi.NULL:
            processed_size[0] = psize

        data[0:psize] = buf[0:psize]
        log.debug("processed size: {}".format(psize))

        return HRESULT.S_OK.value

    def Seek(self, me, offset, origin, newposition):
        log.debug("Seek offset=%d; origin=%d", offset, origin)
        newpos = self.filelike.seek(offset, origin)
        if newposition != ffi.NULL:
            newposition[0] = newpos
        log.debug("new position: %d", newpos)
        return HRESULT.S_OK.value


class FileOutStream(IUnknownImpl):
    """
    Implementation of IOutStream and ISequentialOutStream on top of Python file-like objects.

    Creator is responsible for flushing/closing the file-like object
    """

    GUIDS = {
        IID_IOutStream: "IOutStream",
        IID_ISequentialOutStream: "ISequentialOutStream",
    }

    def __init__(self, file: BinaryIO | PathLike | str) -> None:
        if isinstance(file, (PathLike, str)):
            self.filelike: BinaryIO = open(file, "wb")
        else:
            self.filelike = file
        super().__init__()

    def Write(self, me, data, size, processed_size):
        log.debug("Write %d", size)
        data_arr = ffi.cast("uint8_t*", data)
        buf = bytes(data_arr[0:size])
        # log.debug('data: %s' % buf.decode('ascii'))
        _processed_size = self.filelike.write(buf)
        processed_size[0] = _processed_size
        log.debug("processed_size: %d", _processed_size)
        return HRESULT.S_OK.value

    def Seek(self, me, offset, origin, newposition):
        log.debug("Seek offset=%d; origin=%d", offset, origin)
        newpos = self.filelike.seek(offset, origin)
        if newposition != ffi.NULL:
            newposition[0] = newpos
        log.debug("new position: %d", newpos)
        return HRESULT.S_OK.value
