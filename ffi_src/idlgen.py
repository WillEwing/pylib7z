#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from pathlib import Path
from re import match
from typing import Generator, TextIO

from interfaces import *

INTERFACES_BY_NAME = {interface.name: interface for interface in INTERFACES}


def load_text(filename: str) -> str:
    return (Path(__file__).parent / filename).read_text("utf-8")


class InterfaceNames:
    @property
    def vtable_struct(self) -> str:
        return f"FFI7Z_{self.interface.name}_vtable"

    @property
    def opaque_impl_struct(self) -> str:
        return f"FFI7Z_{self.interface.name}"

    @property
    def python_impl_struct(self) -> str:
        return f"FFI7Z_Py{self.interface.name}"

    @property
    def python_impl_vtable(self) -> str:
        return f"FFI7Z_Py{self.interface.name}_vtable"

    def __init__(self, interface: Interface) -> None:
        self.interface = interface


def format_decotype(decotype: DecoratedType) -> str:
    return f"{decotype.dtype}{decotype.decor}"


def append_vtable_method_cdecl(stream: TextIO, method: Method) -> None:
    args_str = ", ".join(("void* this", *(f"{format_decotype(dt)} {name}" for dt, name in method.arguments)))
    stream.write(f"    {method.return_type} (WINAPI * {method.name})({args_str});\n")


def append_vtable_interface_cdecl(stream: TextIO, interface: Interface) -> None:
    interface_names = InterfaceNames(interface)
    stream.write(f"typedef struct {interface_names.vtable_struct}_tag {{")
    if interface.all_methods:
        stream.write("\n")
        for method in interface.all_methods:
            append_vtable_method_cdecl(stream, method)
    stream.write(f"}} {interface_names.vtable_struct};\n\n")


def append_opaque_impl_cdecl(stream: TextIO, interface: Interface) -> None:
    interface_names = InterfaceNames(interface)
    stream.write(f"typedef struct {interface_names.opaque_impl_struct}_tag {{\n")
    stream.write(f"    {interface_names.vtable_struct}* vtable;\n")
    stream.write(f"}} {interface_names.opaque_impl_struct};\n\n")


def append_python_impl_cdecl(stream: TextIO, interface: Interface) -> None:
    interface_names = InterfaceNames(interface)
    stream.write(f"typedef struct {interface_names.python_impl_struct}_tag {{\n")
    stream.write(f"    {interface_names.vtable_struct}* vtable;\n")
    stream.write(f"    void *self_handle;\n")
    stream.write(f"}} {interface_names.python_impl_struct};\n\n")
    stream.write(f"const {interface_names.vtable_struct} {interface_names.python_impl_vtable};\n\n")


def thunk_name(interface, method) -> str:
    return f"FFI7Z_Py_{interface.name}_{method.name}"


def append_thunk_method_cdecl(stream: TextIO, interface: Interface, method: Method) -> None:
    args_str = ", ".join(("void* this", *(f"{format_decotype(dt)} {name}" for dt, name in method.arguments)))
    stream.write(f"{method.return_type} {thunk_name(interface, method)}({args_str});\n")


def append_interface_thunk_cdecls(stream: TextIO, interface: Interface) -> None:
    for method in interface.methods:
        append_thunk_method_cdecl(stream, interface, method)


def append_thunk_cdecls(stream: TextIO) -> None:
    for interface in INTERFACES:
        append_interface_thunk_cdecls(stream, interface)


def append_thunk_vtable(stream: TextIO, interface: Interface) -> None:
    interface_names = InterfaceNames(interface)
    stream.write(f"const {interface_names.vtable_struct} {interface_names.python_impl_vtable} {{\n")
    for method_origin, method in interface.all_methods_with_origin:
        stream.write(f"    .{method.name} = {thunk_name(method_origin, method)},\n")
    stream.write(f"}};\n\n")


def append_thunk_vtables(stream: TextIO) -> None:
    for interface in INTERFACES:
        append_thunk_vtable(stream, interface)


def append_common_cdecls(stream: TextIO) -> None:
    for interface in INTERFACES:
        append_vtable_interface_cdecl(stream, interface)
        append_opaque_impl_cdecl(stream, interface)
        append_python_impl_cdecl(stream, interface)


def append_static_cdefs(stream: TextIO) -> None:
    stream.write(load_text("ffi77z_static.cdef"))


def append_cdefs(stream: TextIO) -> None:
    append_static_cdefs(stream)
    append_common_cdecls(stream)
    stream.write('extern "Python" {\n')
    append_thunk_cdecls(stream)
    stream.write("}\n\n")


def append_static_cimpl(stream: TextIO) -> None:
    stream.write(load_text("ffi7z_static.c"))


def append_cimpl(stream: TextIO) -> None:
    append_static_cimpl(stream)
    append_common_cdecls(stream)
    append_thunk_cdecls(stream)
    stream.write("\n")
    append_thunk_vtables(stream)


def main() -> None:
    from sys import stdout

    append_cimpl(stdout)
    pass


if __name__ == "__main__":
    main()
