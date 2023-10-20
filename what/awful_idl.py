#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from struct import unpack_from
from typing import Optional
from uuid import UUID as GUID

import pycparser

Argument = tuple[str, str]


def CGUID(guid: GUID) -> str:
    guid_bytes = guid.bytes
    data1, data2, data3, *data4 = unpack_from(">IHH8B", guid_bytes)
    data4_inner_str = ", ".join(f"{byte:#04x}" for byte in data4)
    return f"{{ {data1:#010x}, {data2:#06x}, {data3:#06x}, {{ {data4_inner_str} }} }}"


def Make7ZIID(x, y) -> GUID:
    if not (0 <= x and x <= 255 and 0 <= y and y <= 255):
        raise ValueError("Value out of range.")
    return GUID(f"{{23170F69-40C1-278A-0000-00{x:02x}00{y:02x}0000}}")


@dataclass
class Method:
    name: str
    arguments: list[Argument]
    return_type: str

    def __init__(self, name: str, arguments: list[Argument], return_type="HRESULT") -> None:
        self.name = name
        self.arguments = arguments
        self.return_type = return_type


@dataclass
class Interface:
    name: str
    guid: GUID
    parent: Optional["Interface"]
    methods: list[Method]

    @property
    def vtable_name(self) -> str:
        return f"FFI7Z_{self.name}_vtable"

    @property
    def base_struct_name(self) -> str:
        return f"FFI7Z_{self.name}"

    @property
    def py_impl_struct_name(self) -> str:
        return f"FFI7Z_Py{self.name}"

    @property
    def all_methods(self) -> list[Method]:
        if self.parent:
            return self.parent.all_methods + self.methods
        return self.methods

    @property
    def all_methods_with_origin(self) -> list[tuple["Interface", Method]]:
        methods_with_origin = [(self, method) for method in self.methods]
        if self.parent:
            methods_with_origin = self.parent.all_methods_with_origin + methods_with_origin
        return methods_with_origin


# Minimum necessary set of interfaces for archive extraction:
# - IArchiveExtractCallback
# - IArchiveOpenCallback
# - IArchiveOpenSetSubArchiveName
# - IArchiveOpenVolumeCallback
# - ICompressCodecsInfo
# - ICompressProgressInfo
# - ICryptoGetTextPassword
# - ICryptoGetTextPassword2
# - IInArchive
# - IInStream
# - IOutStream
# - ISequentialInStream
# - ISequentialOutStream
# - ISetCompressCodecsInfo
# - IUnknown


IUnknown = Interface(
    "IUnknown",
    GUID("{00000000-0000-0000-C000-000000000046}"),
    None,
    [
        # STDMETHOD(QueryInterface) (REFIID iid, void **outObject) =0;
        Method(
            "QueryInterface",
            return_type="HRESULT",
            arguments=[
                ("GUID *", "iid"),
                ("void **", "out_object"),
            ],
        ),
        # STDMETHOD_(ULONG, AddRef)() =0;
        Method(
            "AddRef",
            return_type="uint32_t",
            arguments=[],
        ),
        # STDMETHOD_(ULONG, Release)() =0;
        Method(
            "Release",
            return_type="uint32_t",
            arguments=[],
        ),
    ],
)

ISequentialInStream = Interface(
    "ISequentialInStream",
    Make7ZIID(0x03, 0x01),
    IUnknown,
    [
        Method(
            "Read",
            [
                ("void *", "data"),
                ("uint32_t", "size"),
                ("uint32_t *", "processed_size"),
            ],
        ),
    ],
)

IInStream = Interface(
    "IInStream",
    Make7ZIID(0x03, 0x03),
    ISequentialInStream,
    [
        Method(
            "Seek",
            [
                ("int64_t", "offset"),
                ("uint32_t", "seekOrigin"),
                ("uint64_t *", "newPosition"),
            ],
        )
    ],
)

ISequentialOutStream = Interface(
    "ISequentialOutStream",
    Make7ZIID(0x03, 0x02),
    IUnknown,
    [
        Method(
            "Write",
            [
                ("const void *", "data"),
                ("uint32_t", "size"),
                ("uint32_t *", "processed_size"),
            ],
        ),
    ],
)

IOutStream = Interface(
    "IOutStream",
    Make7ZIID(0x03, 0x05),
    ISequentialOutStream,
    [
        Method(
            "Seek",
            [
                ("int64_t", "offset"),
                ("uint32_t", "seekOrigin"),
                ("uint64_t *", "newPosition"),
            ],
        )
    ],
)

IProgress = Interface(
    "IProgress",
    Make7ZIID(0x00, 0x05),
    IUnknown,
    [
        # x(SetTotal(UInt64 total))
        Method(
            "SetTotal",
            [
                ("uint64_t", "total"),
            ],
        ),
        # x(SetCompleted(const UInt64 *completeValue))
        Method(
            "SetCompleted",
            [
                ("const uint64_t *", "complete_value"),
            ],
        ),
    ],
)

IArchiveExtractCallback = Interface(
    "IArchiveExtractCallback",
    Make7ZIID(0x06, 0x20),
    IProgress,
    [
        # x(GetStream(UInt32 index, ISequentialOutStream **outStream, Int32 askExtractMode)) \
        Method(
            "GetStream",
            [
                ("uint32_t", "index"),
                (f"{ISequentialOutStream.base_struct_name} *", "out_stream"),
                ("int32_t", "ask_extract_mode"),
            ],
        ),
        # x(PrepareOperation(Int32 askExtractMode)) \
        Method(
            "PrepareOperation",
            [
                ("int32_t", "ask_extract_mode"),
            ],
        ),
        # x(SetOperationResult(Int32 opRes)) \
        Method(
            "SetOperationResult",
            [
                ("int32_t", "op_result"),
            ],
        ),
    ],
)

IArchiveOpenCallback = Interface(
    "IArchiveOpenCallback",
    Make7ZIID(0x06, 0x10),
    IUnknown,
    [
        # x(SetTotal(const UInt64 *files, const UInt64 *bytes))
        Method(
            "SetTotal",
            [
                ("const uint64_t *", "files"),
                ("const uint64_t *", "bytes"),
            ],
        ),
        # x(SetCompleted(const UInt64 *files, const UInt64 *bytes))
        Method(
            "SetCompleted",
            [
                ("const uint64_t *", "files"),
                ("const uint64_t *", "bytes"),
            ],
        ),
    ],
)

IArchiveOpenSetSubArchiveName = Interface(
    "IArchiveOpenSetSubArchiveName",
    Make7ZIID(0x06, 0x50),
    IUnknown,
    [
        # x(SetSubArchiveName(const wchar_t *name))
        Method(
            "SetSubArchiveName",
            [
                ("const wchar_t *", "name"),
            ],
        )
    ],
)

IArchiveOpenVolumeCallback = Interface(
    "IArchiveOpenVolumeCallback",
    Make7ZIID(0x06, 0x30),
    IUnknown,
    [
        # x(GetProperty(PROPID propID, PROPVARIANT *value))
        Method(
            "GetProperty",
            [
                ("PROPID", "prop_id"),
                ("PROPVARIANT *", "value"),
            ],
        ),
        # x(GetStream(const wchar_t *name, IInStream **inStream))
        Method(
            "GetStream",
            [
                ("const wchar_t *", "name"),
                (f"{IInStream.base_struct_name} **", "in_stream"),
            ],
        ),
    ],
)

ICompressCodecsInfo = Interface(
    "ICompressCodecsInfo",
    Make7ZIID(0x04, 0x60),
    IUnknown,
    [
        # x(GetNumMethods(UInt32 *numMethods))
        Method(
            "GetNumMethods",
            [
                ("uint32_t *", "num_methods"),
            ],
        ),
        # x(GetProperty(UInt32 index, PROPID propID, PROPVARIANT *value))
        Method(
            "GetProperty",
            [
                ("uint32_t", "index"),
                ("PROPID", "prop_id"),
                ("PROPVARIANT *", "value"),
            ],
        ),
        # x(CreateDecoder(UInt32 index, const GUID *iid, void* *coder))
        Method(
            "CreateDecoder",
            [
                ("uint32_t", "index"),
                ("const GUID *", "iid"),
                ("void **", "coder"),
            ],
        ),
        # x(CreateEncoder(UInt32 index, const GUID *iid, void* *coder))
        Method(
            "CreateEncoder",
            [
                ("uint32_t", "index"),
                ("const GUID *", "iid"),
                ("void **", "coder"),
            ],
        ),
    ],
)

ICompressProgressInfo = Interface(
    "ICompressProgressInfo",
    Make7ZIID(0x04, 0x04),
    IUnknown,
    [
        # x(SetRatioInfo(const UInt64 *inSize, const UInt64 *outSize))
        Method(
            "SetRatioInfo",
            [
                ("const uint64_t *", "in_size"),
                ("const uint64_t *", "out_size"),
            ],
        )
    ],
)

ICryptoGetTextPassword = Interface(
    "ICryptoGetTextPassword",
    Make7ZIID(0x05, 0x10),
    IUnknown,
    [
        # x(CryptoGetTextPassword(BSTR *password))
        Method(
            "CryptoGetTextPassword",
            [
                ("wchar_t **", "password"),
            ],
        )
    ],
)

ICryptoGetTextPassword2 = Interface(
    "ICryptoGetTextPassword2",
    Make7ZIID(0x05, 0x11),
    IUnknown,
    [
        # x(CryptoGetTextPassword2(Int32 *passwordIsDefined, BSTR *password))
        Method(
            "CryptoGetTextPassword2",
            [
                ("int32_t *", "password_is_defined"),
                ("wchar_t **", "password"),
            ],
        )
    ],
)

IInArchive = Interface(
    "IInArchive",
    Make7ZIID(0x06, 0x60),
    IUnknown,
    [
        # x(Open(IInStream *stream, const UInt64 *maxCheckStartPosition, IArchiveOpenCallback *openCallback))
        Method(
            "Open",
            [
                (f"{IInStream.base_struct_name} *", "stream"),
                ("const uint64_t *", "max_check_start_position"),
                (f"{IArchiveOpenCallback.base_struct_name} *", "open_callback"),
            ],
        ),
        # x(Close())
        Method("Close", []),
        # x(GetNumberOfItems(UInt32 *numItems))
        Method(
            "GetNumberOfItems",
            [
                ("uint32_t *", "num_items"),
            ],
        ),
        # x(GetProperty(UInt32 index, PROPID propID, PROPVARIANT *value))
        Method(
            "GetProperty",
            [
                ("uint32_t", "index"),
                ("PROPID", "prop_id"),
                ("PROPVARIANT *", "value"),
            ],
        ),
        # x(Extract(const UInt32 *indices, UInt32 numItems, Int32 testMode, IArchiveExtractCallback *extractCallback))
        Method(
            "Extract",
            [
                ("const uint32_t *", "indices"),
                ("uint32_t", "num_items"),
                ("int32_t", "test_mode"),
                (f"{IArchiveExtractCallback.base_struct_name} *", "extract_callback"),
            ],
        ),
        # x(GetArchiveProperty(PROPID propID, PROPVARIANT *value))
        Method(
            "GetArchiveProperty",
            [
                ("PROPID", "prop_id"),
                ("PROPVARIANT *", "value"),
            ],
        ),
        # x(GetNumberOfProperties(UInt32 *numProps))
        Method(
            "GetNumberOfProperties",
            [
                ("uint32_t *", "num_props"),
            ],
        ),
        # x(GetPropertyInfo(UInt32 index, BSTR *name, PROPID *propID, VARTYPE *varType))
        Method(
            "GetPropertyInfo",
            [
                ("uint32_t", "index"),
                ("wchar_t **", "name"),
                ("PROPID *", "prop_id"),
                ("VARTYPE *", "var_type"),
            ],
        ),
        # x(GetNumberOfArchiveProperties(UInt32 *numProps))
        Method(
            "GetNumberOfArchiveProperties",
            [
                ("uint32_t *", "num_properties"),
            ],
        ),
        # x(GetArchivePropertyInfo(UInt32 index, BSTR *name, PROPID *propID, VARTYPE *varType))
        Method(
            "GetArchivePropertyInfo",
            [
                ("uint32_t", "index"),
                ("wchar_t **", "name"),
                ("PROPID *", "prop_id"),
                ("VARTYPE *", "var_type"),
            ],
        ),
    ],
)


ISetCompressCodecsInfo = Interface(
    "ISetCompressCodecsInfo",
    Make7ZIID(0x40, 0x61),
    IUnknown,
    [
        # x(SetCompressCodecsInfo(ICompressCodecsInfo *compressCodecsInfo))
        Method(
            "SetCompressCodecsInfo",
            [
                (f"{ICompressCodecsInfo.base_struct_name} *", "compress_codecs_info"),
            ],
        )
    ],
)

INTERFACES = [
    IUnknown,
    ISequentialInStream,
    IInStream,
    ISequentialOutStream,
    IOutStream,
    IProgress,
    IArchiveExtractCallback,
    IArchiveOpenCallback,
    IArchiveOpenSetSubArchiveName,
    IArchiveOpenVolumeCallback,
    ICompressCodecsInfo,
    ICompressProgressInfo,
    ICryptoGetTextPassword,
    ICryptoGetTextPassword2,
    IInArchive,
    ISetCompressCodecsInfo,
]


def gen_common():
    for interface in INTERFACES:
        yield f"typedef struct {interface.vtable_name}_tag {{"
        for method in interface.all_methods:
            method_args = ", ".join(f"{a} {b}" for a, b in (("void*", "self"), *method.arguments))
            yield f"    {method.return_type} (WINAPI *{method.name})({method_args});"
        yield f"}} {interface.vtable_name};"
        yield ""
        yield f"typedef struct {interface.base_struct_name}_tag {{"
        yield f"    {interface.vtable_name} * vtable;"
        yield f"}} {interface.base_struct_name};"
        yield ""
        yield f"typedef struct {interface.py_impl_struct_name}_tag {{"
        yield f"    {interface.vtable_name} * vtable;"
        yield f"    void * pyojbect_tag;"
        yield f"}} {interface.py_impl_struct_name};"
        yield ""


def gen_cdefs():
    yield ("/* - BEGIN GENERATED CDEFS - */")
    yield from gen_common()
    yield ""
    for interface in INTERFACES:
        yield f"const GUID FFI7Z_IID_{interface.name};"
        yield f"const {interface.vtable_name} {interface.py_impl_struct_name}_vtable;"
        yield ""
    yield 'extern "Python" {'
    for interface in INTERFACES:
        for method in interface.methods:
            args_str = ", ".join(f"{a} {b}" for a, b in (("void*", "self"), *method.arguments))
            yield f"{method.return_type} WINAPI FFI7Z_Py_{interface.name}_{method.name}({args_str});"
    yield "}"
    yield ("/* - END GENERATED CDEFS - */")


def make_cdefs():
    return "\n".join(gen_cdefs())


def gen_cimpl():
    yield ("/* - BEGIN GENERATED CIMPL - */")
    yield from gen_common()
    yield ""
    for interface in INTERFACES:
        for method in interface.methods:
            args_str = ", ".join(f"{a} {b}" for a, b in (("void*", "self"), *method.arguments))
            yield f"{method.return_type} WINAPI FFI7Z_Py_{interface.name}_{method.name}({args_str});"
    yield ""
    for interface in INTERFACES:
        yield f"const GUID FFI7Z_IID_{interface.name} = {CGUID(interface.guid)};"
        yield ""
        yield f"const {interface.vtable_name} {interface.py_impl_struct_name}_vtable = {{"
        for origin_intf, method in interface.all_methods_with_origin:
            yield f"  .{method.name} = FFI7Z_Py_{origin_intf.name}_{method.name},"
        yield f"}};"
        yield ""
    yield ("/* - END GENERATED CIMPL - */")


def make_cimpl():
    return "\n".join(gen_cimpl())


def gen_py_thunks():
    yield "#!/usr/bin/env python"
    yield "# -*- coding: utf-8 -*-"
    yield ""
    yield "from _ffi7z import lib, ffi"
    yield ""
    for interface in INTERFACES:
        for method in interface.methods:
            yield f"@ffi.def_extern()"
            args_string = ", ".join(f"{b}" for a, b in (("void *", "this"), *method.arguments))
            pass_args_string = ", ".join(f"{b}" for a, b in method.arguments)
            yield f"def FFI7Z_Py_{interface.name}_{method.name}({args_string}):"
            yield f'    this_struct = ffi.cast("{interface.py_impl_struct_name} *", this)'
            yield f"    self = ffi.from_handle(this_struct[0].pyobject_tag)"
            yield f"    return self.{method.name}({pass_args_string})"
            yield ""


def make_py_thunks():
    return "\n".join(gen_py_thunks())


def main():
    with open("ffi7z_com.cdef", "w", encoding="utf-8") as cdefs_file:
        cdefs_file.write(make_cdefs())
    with open("ffi7z_com.inl", "w", encoding="utf-8") as cimpl_file:
        cimpl_file.write(make_cimpl())
    with open("ffi7z_thunk.py", "w", encoding="utf-8") as pythunk_file:
        pythunk_file.write(make_py_thunks())


if __name__ == "__main__":
    main()
