#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
from setuptools import setup

from ffi7zip.build_ffi7zip import ffibuilder

setup(ext_modules=[(ffibuilder.distutils_extension())])
