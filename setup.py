#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import os.path
import sys

import setuptools

sys.path.append(os.path.dirname(__file__))

from ffi7zip.build_ffi7zip import ffibuilder

setuptools.setup(ext_modules=[(ffibuilder.distutils_extension())])
