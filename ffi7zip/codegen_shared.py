#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""
Generate C source and definitions from `interfaces.py`
"""

from .interfaces import CInterface, CMethod


class InterfaceNames:
    """
    Helper class to get interface struct and instance names.
    """

    @property
    def vtable_struct(self) -> str:
        """
        Virtual function table struct name.
        """
        return f"FFI7Z_{self.interface.name}_vtable"

    @property
    def opaque_impl_struct(self) -> str:
        """
        Opaque implementation struct name.
        """
        return f"FFI7Z_{self.interface.name}"

    @property
    def python_impl_struct(self) -> str:
        """
        Python implementation struct name.
        """
        return f"FFI7Z_Py{self.interface.name}"

    @property
    def python_impl_vtable(self) -> str:
        """
        Python implemenation vtable instance name.
        """
        return f"FFI7Z_Py{self.interface.name}_vtable"

    def __init__(self, interface: CInterface) -> None:
        self.interface = interface


def thunk_name(interface: CInterface, method: CMethod) -> str:
    """
    Get the name of a the thunk for `interface`.`method`.
    """
    return f"FFI7Z_Py_{interface.name}_{method.name}"
