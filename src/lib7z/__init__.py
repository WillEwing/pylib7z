#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python bindings for the 7-Zip Library
"""

import ctypes.util
import os
import os.path
import sys

from . import thunks  # noqa
from .ffi7z import ffi, lib  # pylint: disable=no-name-in-module


def load_lib7z():
    """
    Find and load the 7-zip DLL.
    """
    dll_paths = []

    if "7ZDLL_PATH" in os.environ:
        dll_paths.append(os.environ["7ZDLL_PATH"])

    if sys.platform == "win32":
        try:
            from winreg import (  # pylint: disable=import-outside-toplevel
                HKEY_LOCAL_MACHINE,
                KEY_READ,
                OpenKey,
                QueryValueEx,
            )

            key = OpenKey(HKEY_LOCAL_MACHINE, "SOFTWARE\\7-zip", 0, KEY_READ)
            install_dir = QueryValueEx(key, "Path")[0]
            dll_paths.append(os.path.join(install_dir, "7z.dll"))
        except WindowsError:
            pass

    if found_lib := ctypes.util.find_library("7z"):
        dll_paths.append(found_lib)

    for dll_path in dll_paths:
        hresult = lib.InitModule(dll_path)
        if hresult >= 0:
            break
    else:
        raise RuntimeError("Could not load 7-zip library.")


ffi.init_once(load_lib7z, __package__)


from .archive import Archive, ArchiveItem  # pylint: disable=wrong-import-position
