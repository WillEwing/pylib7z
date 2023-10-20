#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from cffi import FFI


def load_text(filename: str) -> str:
    return (Path(__file__).parent / filename).read_text("utf-8")


ffibuilder = FFI()
ffibuilder.set_source("_ffi7z", load_text("ffi7z.c"), libraries=["Ole32"])


for name in ("types", "module"):
    ffibuilder.cdef(load_text(f"ffi7z_{name}.cdef"))


def main():
    ffibuilder.compile("_ffi7z", verbose=1, target="_ffi7z.*")


if __name__ == "__main__":
    main()
