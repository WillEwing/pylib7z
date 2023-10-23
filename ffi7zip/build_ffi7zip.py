#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""
Python bindings for 7-zip: FFI Builder.
"""

from io import StringIO
from typing import Optional

from cffi import FFI
from setuptools import Command  # pylint: disable=import-error

from .codegen_py import build_thunks_py
from .idlgen import append_cdefs, append_cimpl


def get_cimpl() -> str:
    """
    Get C implementation source.
    """
    stream = StringIO()
    append_cimpl(stream)
    return stream.getvalue()


def get_cdefs() -> str:
    """
    Get IDL C definitions.
    """
    stream = StringIO()
    append_cdefs(stream)
    return stream.getvalue()


ffibuilder = FFI()
ffibuilder.set_unicode(True)
ffibuilder.set_source("lib7zip.ffi7zip", get_cimpl(), libraries=["Ole32", "OleAut32"])
ffibuilder.cdef(get_cdefs())


class UpdateThunks(Command):
    """
    Subcommand for setuptools to update thunks from IDL.
    """

    build_lib: Optional[str]
    editable_mode: bool

    def initialize_options(self) -> None:
        """Initialize options?"""
        self.build_lib = None
        self.editable_mode = False

    def finalize_options(self) -> None:
        """Finalize options?"""
        self.set_undefined_options("build_py", ("build_lib", "build_lib"))

    def run(self) -> None:
        """Generated updated thunks file."""
        thunks_path = "lib7zip/thunks.py"
        with open(thunks_path, "wb") as thunks_py:
            thunks_py.write(build_thunks_py())
