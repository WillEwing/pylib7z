#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from dataclasses import dataclass
from functools import cache, cached_property
from struct import unpack_from
from typing import Any, Generator, NamedTuple, Optional
from uuid import UUID as GUID

from pycparser.c_lexer import CLexer

is_c_ident = re.compile("[A-Za-z_][0-9A-Za-z_]*").match


def Make7ZIID(x, y) -> GUID:
    if not (0 <= x and x <= 255 and 0 <= y and y <= 255):
        raise ValueError("Value out of range.")
    return GUID(f"{{23170F69-40C1-278A-0000-00{x:02x}00{y:02x}0000}}")


class CTypeDecl:
    """
    A tokenized of a (restricted subset of a) C type definition.
    """

    def __error_func(self, msg, start, end):
        raise ValueError("%s [%d:%d]", msg, start, end)

    def __unexpected(self, *args):
        raise ValueError("Unexpected brace.")

    def __assume_type_valid(self, *args):
        return True

    def __init__(self, raw_ctype_decl: str | list[str]) -> None:
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
        self.tokens: list[str] = []
        while True:
            next_token = lexer.token()
            if next_token is None:
                break
            self.tokens.append(next_token.value)

    def __repr__(self) -> str:
        self_str = str(self)
        return f"{self.__class__.__name__}({self_str!r})"

    @cache
    def __str__(self) -> str:
        value = ""
        for token in self.tokens:
            if value and is_c_ident(token):
                value += " "
            value += token
        return value


class Argument(NamedTuple):
    dtype: CTypeDecl
    name: str


@dataclass
class Method:
    def __init__(self, name: str, arguments: list[tuple[CTypeDecl | str, str]], return_type: str = "HRESULT"):
        self.name = name
        self.return_type = return_type
        self.arguments = [(CTypeDecl(str(dtype)), name) for dtype, name in arguments]

    name: str
    arguments: list[Argument]
    return_type: str


@dataclass
class Interface:
    name: str
    guid: GUID
    parent: Optional["Interface"]
    methods: list[Method]

    @property
    def all_methods_with_origin(self) -> Generator[tuple["Interface", Method], None, None]:
        if self.parent:
            yield from self.parent.all_methods_with_origin
        yield from ((self, method) for method in self.methods)

    @property
    def all_methods(self) -> Generator[Method, None, None]:
        yield from (method for intf, method in self.all_methods_with_origin)


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
                ("ISequentialOutStream **", "out_stream"),
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
                ("IInStream **", "in_stream"),
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
                ("IInStream *", "stream"),
                ("const uint64_t *", "max_check_start_position"),
                ("IArchiveOpenCallback *", "open_callback"),
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
                ("IArchiveExtractCallback *", "extract_callback"),
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


if __name__ == "__main__":
    from pprint import pprint

    pprint(INTERFACES)
