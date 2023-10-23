#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""
Generate C source and definitions, and Python thunks from `interfaces.py`
"""


import importlib.resources
import sys
from typing import TextIO

from .interfaces import INTERFACES, CInterface, CMethod, CTypeDecl

INTERFACES_BY_NAME = {interface.name: interface for interface in INTERFACES}

if tuple(sys.version_info[:2]) < (3, 11):

    def load_text(filename: str) -> str:
        """Load text from module resource."""
        return importlib.resources.read_text(__package__, filename)

else:

    def load_text(filename: str) -> str:
        """Load text from module resource."""
        return importlib.resources.files(__package__).joinpath(filename).read_text()


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


def mangle_dtype(typedecl: CTypeDecl) -> CTypeDecl:
    """
    Mangles interface names in CTypeDecls.
    """
    tokens = []
    for token in typedecl.tokens:
        interface_type = INTERFACES_BY_NAME.get(token, None)
        if interface_type:
            tokens.append(InterfaceNames(interface_type).opaque_impl_struct)
        else:
            tokens.append(token)
    return CTypeDecl(tokens)


def append_vtable_method_cdecl(stream: TextIO, method: CMethod) -> None:
    """
    Append declaration of vtable method `method` to `stream`.
    """
    args_str = ", ".join(("void* this", *(f"{mangle_dtype(dt)} {name}" for dt, name in method.arguments)))
    stream.write(f"    {method.return_type} (WINAPI * {method.name})({args_str});\n")


def append_vtable_interface_cdecl(stream: TextIO, interface: CInterface) -> None:
    """
    Append declaration of vtable struct for `interface` to `stream`.
    """
    interface_names = InterfaceNames(interface)
    stream.write(f"typedef struct {interface_names.vtable_struct}_tag {{")
    if interface.all_methods:
        stream.write("\n")
        for method in interface.all_methods:
            append_vtable_method_cdecl(stream, method)
    stream.write(f"}} {interface_names.vtable_struct};\n\n")


def append_opaque_impl_cdecl(stream: TextIO, interface: CInterface) -> None:
    """
    Append declaration of opaque implementation struct for `interface` to `stream`.
    """
    interface_names = InterfaceNames(interface)
    stream.write(f"typedef struct {interface_names.opaque_impl_struct}_tag {{\n")
    stream.write(f"    {interface_names.vtable_struct}* vtable;\n")
    stream.write(f"}} {interface_names.opaque_impl_struct};\n\n")


def append_python_impl_cdecl(stream: TextIO, interface: CInterface) -> None:
    """
    Append declaration of Python implementation struct and vtable for `interface` to `stream`.
    """
    interface_names = InterfaceNames(interface)
    stream.write(f"typedef struct {interface_names.python_impl_struct}_tag {{\n")
    stream.write(f"    {interface_names.vtable_struct}* vtable;\n")
    stream.write("    void *self_handle;\n")
    stream.write(f"}} {interface_names.python_impl_struct};\n\n")
    stream.write(f"const {interface_names.vtable_struct} {interface_names.python_impl_vtable};\n\n")


def thunk_name(interface, method) -> str:
    """
    Get the name of a the thunk for `interface`.`method`.
    """
    return f"FFI7Z_Py_{interface.name}_{method.name}"


def append_thunk_method_cdecl(stream: TextIO, interface: CInterface, method: CMethod) -> None:
    """
    Append thunk method declarations for `interface`.`method` to `stream`.
    """
    args_str = ", ".join(("void* this", *(f"{mangle_dtype(dt)} {name}" for dt, name in method.arguments)))
    stream.write(f"{method.return_type} {thunk_name(interface, method)}({args_str});\n")


def append_interface_thunk_cdecls(stream: TextIO, interface: CInterface) -> None:
    """
    Append thunk method declarations for `interface` to `stream`.
    """
    for method in interface.methods:
        append_thunk_method_cdecl(stream, interface, method)


def append_thunk_cdecls(stream: TextIO) -> None:
    """
    Append thunk method declarations to `stream`.
    """
    for interface in INTERFACES:
        append_interface_thunk_cdecls(stream, interface)


def append_thunk_vtable(stream: TextIO, interface: CInterface) -> None:
    """
    Append the thunk vtable definition for `interface` to `stream`.
    """
    interface_names = InterfaceNames(interface)
    stream.write(f"const {interface_names.vtable_struct} {interface_names.python_impl_vtable} = {{\n")
    for method_origin, method in interface.all_methods_with_origin:
        stream.write(f"    .{method.name} = {thunk_name(method_origin, method)},\n")
    stream.write("};\n\n")


def append_thunk_vtables(stream: TextIO) -> None:
    """
    Append thunk vtable definitions to `stream`.
    """
    for interface in INTERFACES:
        append_thunk_vtable(stream, interface)


def append_common_cdecls(stream: TextIO) -> None:
    """
    Append common C declarations to `stream`.
    """
    for interface in INTERFACES:
        append_vtable_interface_cdecl(stream, interface)
        append_opaque_impl_cdecl(stream, interface)
        append_python_impl_cdecl(stream, interface)


def append_static_cdefs(stream: TextIO) -> None:
    """
    Append static C definitions to `stream`.
    """
    stream.write(load_text("ffi7z_static.cdef"))


def append_cdefs(stream: TextIO) -> None:
    """
    Append C definitions to `stream`.
    """
    append_static_cdefs(stream)
    append_common_cdecls(stream)
    stream.write('extern "Python" {\n')
    append_thunk_cdecls(stream)
    stream.write("}\n\n")


def append_static_cimpl(stream: TextIO) -> None:
    """
    Append the static C sources to `stream`.
    """
    stream.write(load_text("ffi7z_static.c"))


def append_cimpl(stream: TextIO) -> None:
    """
    Append C sources to `stream`.
    """
    append_static_cimpl(stream)
    append_common_cdecls(stream)
    append_thunk_cdecls(stream)
    stream.write("\n")
    append_thunk_vtables(stream)
