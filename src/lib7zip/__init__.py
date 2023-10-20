#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python bindings for the 7-Zip Library
"""

import logging

log = logging.getLogger("lib7zip")

from dataclasses import dataclass

from .ffi7z import *


@dataclass
class Method:
    id: int
    name: str
    encoder: GUID | None
    decoder: GUID | None


def get_method_info(index: int) -> Method:
    encoder_is_assigned = GetMethodProperty(index, MethodProps.kEncoderIsAssigned)
    decoder_is_assigned = GetMethodProperty(index, MethodProps.kDecoderIsAssigned)
    return Method(
        id=GetMethodProperty(index, MethodProps.kID),
        name=GetMethodProperty(index, MethodProps.kName),
        encoder=GetMethodProperty(index, MethodProps.kEncoder, UnwrapPropGUID) if encoder_is_assigned else None,
        decoder=GetMethodProperty(index, MethodProps.kDecoder, UnwrapPropGUID) if decoder_is_assigned else None,
    )


def get_methods() -> list[Method]:
    num_methods = GetNumberOfMethods()
    return [get_method_info(index) for index in range(num_methods)]


@dataclass
class Format:
    index: int
    name: str
    classid: GUID
    extensions: tuple[str, ...]
    signatures: tuple[bytes, ...]
    signature_offset: int


def unpack_multi_signature(packed: bytes) -> tuple[bytes, ...]:
    offset = 0
    signatures = []
    while offset < len(packed):
        size = packed[offset]
        next_offset = offset + size + 1
        signatures.append(packed[offset + 1, next_offset])
        offset = next_offset
    return tuple(signatures)


def get_format_info(index: int) -> Format:
    signatures = tuple()

    if not signatures:
        try:
            signatures = GetFormatProperty(index, FormatProps.kMultiSignature, UnwrapPropMultiSig)
        except PropUnwrapError:
            pass

    if not signatures:
        try:
            signatures = (GetFormatProperty(index, FormatProps.kSignature, UnwrapPropBytesZ),)
        except PropUnwrapError:
            pass

    return Format(
        index=index,
        name=GetFormatProperty(index, FormatProps.kName),
        classid=GetFormatProperty(index, FormatProps.kClassID, UnwrapPropGUID),
        extensions=tuple(GetFormatProperty(index, FormatProps.kExtension).split()),
        signatures=signatures,
        signature_offset=GetFormatProperty(index, FormatProps.kSignatureOffset),
    )


def get_formats() -> list[Format]:
    num_formats = GetNumberOfFormats()
    return [get_format_info(index) for index in range(num_formats)]


methods = get_methods()
formats = get_formats()


from .archive import Archive, ArchiveItem
