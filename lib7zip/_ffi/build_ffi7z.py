#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from cffi import FFI


def load_text(filename: str) -> str:
    return (Path(__file__).parent / filename).read_text("utf-8")


ffibuilder = FFI()
ffibuilder.set_source("_ffi7z", load_text("ffi7z.c"), libraries=["Ole32"])


for name in ("types", "module", "com"):
    ffibuilder.cdef(load_text(f"ffi7z_{name}.cdef"))


def main():
    ffibuilder.compile(verbose=1)


if __name__ == "__main__":
    main()
