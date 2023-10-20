# -*- coding: utf-8 -*-
from pathlib import Path

from cffi import FFI
from setuptools import setup


def load_text(filename: str) -> str:
    return (Path(__file__).parent / filename).read_text("utf-8")


ffi7z_ext_cdefs = "\n".join(load_text("lib7zip/ffi7z_%s.cdef" % group) for group in ("types", "module", "com"))
ffi7z_ext_source = "\n".join(load_text("lib7zip/%s" % name) for name in ("ffi7z.c", "ffi7z_com.inl"))

ffi7z_builder = FFI()
ffi7z_builder.cdef(ffi7z_ext_cdefs)
ffi7z_builder.set_source("lib7zip._ffi7z", ffi7z_ext_source, libraries=["Ole32"])

setup(
    ext_modules=[ffi7z_builder.distutils_extension()],
)
