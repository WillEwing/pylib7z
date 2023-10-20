# -*- coding: utf-8 -*-
from setuptools import setup

import lib7zip.ffi7z_builder

setup(
    ext_modules=[lib7zip._ffi7z_builder.ffibuilder.distutils_extension()],
)
