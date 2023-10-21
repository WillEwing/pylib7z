#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import os.path
import sys

import setuptools
import setuptools.command.build

# Latest setuptools/pip removes '' from sys.path, but it's needed here for code generation.
sys.path.append(os.path.dirname(__file__))
from ffi7zip.build_ffi7zip import (  # noqa, pylint: disable=wrong-import-position
    UpdateThunks,
    ffibuilder,
)

setuptools.command.build.build.sub_commands.append(("update_thunks", None))

# Configure and run setuptools.
setuptools.setup(
    ext_modules=[
        ffibuilder.distutils_extension(),  # type: ignore
    ],
    cmdclass={
        "update_thunks": UpdateThunks,
    },
)
