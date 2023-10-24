#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interfaces and embedded IDL for ffi7zip.
"""

import re
from dataclasses import dataclass
from typing import List, NamedTuple, Optional
from uuid import UUID as GUID

from pycparser.c_lexer import CLexer  # type: ignore

is_c_ident = re.compile("[A-Za-z_][0-9A-Za-z_]*").match


def make_7zip_iid(x, y):
    """
    Make an IID for a class in 7z.dll.
    """
    if not (0 <= x and x <= 255 and 0 <= y and y <= 255):
        raise ValueError("Value out of range.")
    return GUID(f"{{23170F69-40C1-278A-0000-00{x:02x}00{y:02x}0000}}")


class CTypeDecl:
    """
    A tokenized of a (restricted subset of a) C type definition.
    """

    def __error_func(self, msg, start, end):
        raise ValueError(f"{msg} [{start}:{end}]")

    def __unexpected(self, *args):
        raise ValueError("Unexpected brace.")

    def __assume_type_valid(self, _):
        return True

    def __init__(self, raw_ctype_decl):
        if not isinstance(raw_ctype_decl, str):
            raw_ctype_decl = " ".join(raw_ctype_decl)
        lexer = CLexer(
            error_func=self.__error_func,
            on_lbrace_func=self.__unexpected,
            on_rbrace_func=self.__unexpected,
            type_lookup_func=self.__assume_type_valid,
        )
        lexer.build()
        lexer.input(raw_ctype_decl)
        self.tokens = []
        while True:
            next_token = lexer.token()
            if next_token is None:
                break
            self.tokens.append(next_token.value)

    def __repr__(self):
        self_str = str(self)
        return f"{self.__class__.__name__}({self_str!r})"

    def __str__(self):
        value = ""
        for token in self.tokens:
            if value and is_c_ident(token):
                value += " "
            value += token
        return value


class CArg(NamedTuple):
    """
    Method argument definition.
    """

    dtype: CTypeDecl
    name: str


@dataclass
class CMethod:
    """
    A method definitoin.
    """

    def __init__(self, name, arguments, return_type="HRESULT"):
        self.name = name
        self.return_type = return_type
        self.arguments = [(CTypeDecl(str(dtype)), name) for dtype, name in arguments]

    name: str
    arguments: List[CArg]
    return_type: str


@dataclass
class CInterface:
    """
    An interface definition.
    """

    name: str
    guid: GUID
    parent: Optional["CInterface"]
    methods: List[CMethod]

    @property
    def all_methods_with_origin(self):
        """
        All of the methods as (originating0interface, method) pairs.
        """
        if self.parent:
            yield from self.parent.all_methods_with_origin
        yield from ((self, method) for method in self.methods)

    @property
    def all_methods(self):
        """
        All of the interface's methods.
        """
        yield from (method for intf, method in self.all_methods_with_origin)


IUnknown = CInterface(
    "IUnknown",
    GUID("{00000000-0000-0000-C000-000000000046}"),
    None,
    [
        # STDMETHOD(QueryInterface) (REFIID iid, void **outObject) =0;
        CMethod(
            "QueryInterface",
            return_type="HRESULT",
            arguments=[
                ("GUID *", "iid"),
                ("void **", "out_object"),
            ],
        ),
        # STDMETHOD_(ULONG, AddRef)() =0;
        CMethod(
            "AddRef",
            return_type="uint32_t",
            arguments=[],
        ),
        # STDMETHOD_(ULONG, Release)() =0;
        CMethod(
            "Release",
            return_type="uint32_t",
            arguments=[],
        ),
    ],
)

ISequentialInStream = CInterface(
    "ISequentialInStream",
    make_7zip_iid(0x03, 0x01),
    IUnknown,
    [
        CMethod(
            "Read",
            [
                ("void *", "data"),
                ("uint32_t", "size"),
                ("uint32_t *", "processed_size"),
            ],
        ),
    ],
)

IInStream = CInterface(
    "IInStream",
    make_7zip_iid(0x03, 0x03),
    ISequentialInStream,
    [
        CMethod(
            "Seek",
            [
                ("int64_t", "offset"),
                ("uint32_t", "seekOrigin"),
                ("uint64_t *", "newPosition"),
            ],
        )
    ],
)

ISequentialOutStream = CInterface(
    "ISequentialOutStream",
    make_7zip_iid(0x03, 0x02),
    IUnknown,
    [
        CMethod(
            "Write",
            [
                ("const void *", "data"),
                ("uint32_t", "size"),
                ("uint32_t *", "processed_size"),
            ],
        ),
    ],
)

IOutStream = CInterface(
    "IOutStream",
    make_7zip_iid(0x03, 0x05),
    ISequentialOutStream,
    [
        CMethod(
            "Seek",
            [
                ("int64_t", "offset"),
                ("uint32_t", "seekOrigin"),
                ("uint64_t *", "newPosition"),
            ],
        )
    ],
)

IProgress = CInterface(
    "IProgress",
    make_7zip_iid(0x00, 0x05),
    IUnknown,
    [
        # x(SetTotal(UInt64 total))
        CMethod(
            "SetTotal",
            [
                ("uint64_t", "total"),
            ],
        ),
        # x(SetCompleted(const UInt64 *completeValue))
        CMethod(
            "SetCompleted",
            [
                ("const uint64_t *", "complete_value"),
            ],
        ),
    ],
)

IArchiveExtractCallback = CInterface(
    "IArchiveExtractCallback",
    make_7zip_iid(0x06, 0x20),
    IProgress,
    [
        # x(GetStream(UInt32 index, ISequentialOutStream **outStream, Int32 askExtractMode)) \
        CMethod(
            "GetStream",
            [
                ("uint32_t", "index"),
                ("ISequentialOutStream **", "out_stream"),
                ("int32_t", "ask_extract_mode"),
            ],
        ),
        # x(PrepareOperation(Int32 askExtractMode)) \
        CMethod(
            "PrepareOperation",
            [
                ("int32_t", "ask_extract_mode"),
            ],
        ),
        # x(SetOperationResult(Int32 opRes)) \
        CMethod(
            "SetOperationResult",
            [
                ("int32_t", "op_result"),
            ],
        ),
    ],
)

IArchiveOpenCallback = CInterface(
    "IArchiveOpenCallback",
    make_7zip_iid(0x06, 0x10),
    IUnknown,
    [
        # x(SetTotal(const UInt64 *files, const UInt64 *bytes))
        CMethod(
            "SetTotal",
            [
                ("const uint64_t *", "files"),
                ("const uint64_t *", "bytes"),
            ],
        ),
        # x(SetCompleted(const UInt64 *files, const UInt64 *bytes))
        CMethod(
            "SetCompleted",
            [
                ("const uint64_t *", "files"),
                ("const uint64_t *", "bytes"),
            ],
        ),
    ],
)

IArchiveOpenSetSubArchiveName = CInterface(
    "IArchiveOpenSetSubArchiveName",
    make_7zip_iid(0x06, 0x50),
    IUnknown,
    [
        # x(SetSubArchiveName(const wchar_t *name))
        CMethod(
            "SetSubArchiveName",
            [
                ("const wchar_t *", "name"),
            ],
        )
    ],
)

IArchiveOpenVolumeCallback = CInterface(
    "IArchiveOpenVolumeCallback",
    make_7zip_iid(0x06, 0x30),
    IUnknown,
    [
        # x(GetProperty(PROPID propID, PROPVARIANT *value))
        CMethod(
            "GetProperty",
            [
                ("PROPID", "prop_id"),
                ("PROPVARIANT *", "value"),
            ],
        ),
        # x(GetStream(const wchar_t *name, IInStream **inStream))
        CMethod(
            "GetStream",
            [
                ("const wchar_t *", "name"),
                ("IInStream **", "in_stream"),
            ],
        ),
    ],
)

ICompressCodecsInfo = CInterface(
    "ICompressCodecsInfo",
    make_7zip_iid(0x04, 0x60),
    IUnknown,
    [
        # x(GetNumMethods(UInt32 *numMethods))
        CMethod(
            "GetNumMethods",
            [
                ("uint32_t *", "num_methods"),
            ],
        ),
        # x(GetProperty(UInt32 index, PROPID propID, PROPVARIANT *value))
        CMethod(
            "GetProperty",
            [
                ("uint32_t", "index"),
                ("PROPID", "prop_id"),
                ("PROPVARIANT *", "value"),
            ],
        ),
        # x(CreateDecoder(UInt32 index, const GUID *iid, void* *coder))
        CMethod(
            "CreateDecoder",
            [
                ("uint32_t", "index"),
                ("const GUID *", "iid"),
                ("void **", "coder"),
            ],
        ),
        # x(CreateEncoder(UInt32 index, const GUID *iid, void* *coder))
        CMethod(
            "CreateEncoder",
            [
                ("uint32_t", "index"),
                ("const GUID *", "iid"),
                ("void **", "coder"),
            ],
        ),
    ],
)

ICompressProgressInfo = CInterface(
    "ICompressProgressInfo",
    make_7zip_iid(0x04, 0x04),
    IUnknown,
    [
        # x(SetRatioInfo(const UInt64 *inSize, const UInt64 *outSize))
        CMethod(
            "SetRatioInfo",
            [
                ("const uint64_t *", "in_size"),
                ("const uint64_t *", "out_size"),
            ],
        )
    ],
)

ICryptoGetTextPassword = CInterface(
    "ICryptoGetTextPassword",
    make_7zip_iid(0x05, 0x10),
    IUnknown,
    [
        # x(CryptoGetTextPassword(BSTR *password))
        CMethod(
            "CryptoGetTextPassword",
            [
                ("wchar_t **", "password"),
            ],
        )
    ],
)

ICryptoGetTextPassword2 = CInterface(
    "ICryptoGetTextPassword2",
    make_7zip_iid(0x05, 0x11),
    IUnknown,
    [
        # x(CryptoGetTextPassword2(Int32 *passwordIsDefined, BSTR *password))
        CMethod(
            "CryptoGetTextPassword2",
            [
                ("int32_t *", "password_is_defined"),
                ("wchar_t **", "password"),
            ],
        )
    ],
)

IInArchive = CInterface(
    "IInArchive",
    make_7zip_iid(0x06, 0x60),
    IUnknown,
    [
        # x(Open(IInStream *stream, const UInt64 *maxCheckStartPosition, IArchiveOpenCallback *openCallback))
        CMethod(
            "Open",
            [
                ("IInStream *", "stream"),
                ("const uint64_t *", "max_check_start_position"),
                ("IArchiveOpenCallback *", "open_callback"),
            ],
        ),
        # x(Close())
        CMethod("Close", []),
        # x(GetNumberOfItems(UInt32 *numItems))
        CMethod(
            "GetNumberOfItems",
            [
                ("uint32_t *", "num_items"),
            ],
        ),
        # x(GetProperty(UInt32 index, PROPID propID, PROPVARIANT *value))
        CMethod(
            "GetProperty",
            [
                ("uint32_t", "index"),
                ("PROPID", "prop_id"),
                ("PROPVARIANT *", "value"),
            ],
        ),
        # x(Extract(const UInt32 *indices, UInt32 numItems, Int32 testMode, IArchiveExtractCallback *extractCallback))
        CMethod(
            "Extract",
            [
                ("const uint32_t *", "indices"),
                ("uint32_t", "num_items"),
                ("int32_t", "test_mode"),
                ("IArchiveExtractCallback *", "extract_callback"),
            ],
        ),
        # x(GetArchiveProperty(PROPID propID, PROPVARIANT *value))
        CMethod(
            "GetArchiveProperty",
            [
                ("PROPID", "prop_id"),
                ("PROPVARIANT *", "value"),
            ],
        ),
        # x(GetNumberOfProperties(UInt32 *numProps))
        CMethod(
            "GetNumberOfProperties",
            [
                ("uint32_t *", "num_props"),
            ],
        ),
        # x(GetPropertyInfo(UInt32 index, BSTR *name, PROPID *propID, VARTYPE *varType))
        CMethod(
            "GetPropertyInfo",
            [
                ("uint32_t", "index"),
                ("wchar_t **", "name"),
                ("PROPID *", "prop_id"),
                ("VARTYPE *", "var_type"),
            ],
        ),
        # x(GetNumberOfArchiveProperties(UInt32 *numProps))
        CMethod(
            "GetNumberOfArchiveProperties",
            [
                ("uint32_t *", "num_properties"),
            ],
        ),
        # x(GetArchivePropertyInfo(UInt32 index, BSTR *name, PROPID *propID, VARTYPE *varType))
        CMethod(
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


ISetCompressCodecsInfo = CInterface(
    "ISetCompressCodecsInfo",
    make_7zip_iid(0x40, 0x61),
    IUnknown,
    [
        # x(SetCompressCodecsInfo(ICompressCodecsInfo *compressCodecsInfo))
        CMethod(
            "SetCompressCodecsInfo",
            [
                ("ICompressCodecsInfo *", "compress_codecs_info"),
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
    ICompressProgressInfo,
    ICryptoGetTextPassword,
    ICryptoGetTextPassword2,
    IInArchive,
]
