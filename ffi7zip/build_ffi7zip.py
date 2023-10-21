#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

from io import StringIO

from cffi import FFI

from .idlgen import append_cdefs, append_cimpl


def get_cimpl() -> str:
    stream = StringIO()
    append_cimpl(stream)
    return stream.getvalue()


def get_cdefs() -> str:
    stream = StringIO()
    append_cdefs(stream)
    return stream.getvalue()


ffibuilder = FFI()
ffibuilder.set_unicode(True)
ffibuilder.set_source("lib7zip.ffi7zip", get_cimpl(), libraries=["Ole32"])
ffibuilder.cdef(get_cdefs())


def main():
    ffibuilder.compile(verbose=True)


if __name__ == "__main__":
    main()
