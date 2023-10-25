#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python bindings for 7-Zip library: method registry.
"""

from collections.abc import Sequence
from enum import IntEnum
from typing import Optional
from uuid import UUID

from .ffi7z import ffi, lib  # pylint: disable=no-name-in-module
from .propvariant import PropVariant


class MethodProps(IntEnum):
    """
    Method properties
    """

    ID = 0
    NAME = 1
    DECODER = 2
    ENCODER = 3
    PACK_STREAMS = 4
    UNPACK_STREAMS = 5
    DESCRIPTION = 6
    DECODER_IS_ASSIGNED = 7
    ENCODER_IS_ASSIGNED = 8
    DIGEST_SIZE = 9
    IS_FILTER = 10


def _get_num_methods() -> int:
    """
    Get the number of methods.
    """
    num_methods_ptr = ffi.new("uint32_t *")
    hresult = lib.GetNumberOfMethods(num_methods_ptr)
    if hresult < 0:
        raise RuntimeError(f"HRESULT: {hresult:#010x}")
    return int(num_methods_ptr[0])


def _get_method_property(index: int, prop_id: int) -> PropVariant:
    """
    Get property `prop_id` of archive method `index`.
    """
    prop_var = PropVariant()
    hresult = lib.GetMethodProperty(index, prop_id, prop_var.cdata)  # type: ignore
    if hresult < 0:
        raise RuntimeError(f"HRESULT: {hresult:#010x}")
    return prop_var


class MethodInfo:
    """
    Method info.
    """

    def __init__(self, index: int) -> None:
        if not (0 <= index < _get_num_methods()):
            raise IndexError()
        self.index = index

    @property
    def id(self) -> int:
        """Method id"""
        return _get_method_property(self.index, MethodProps.ID).as_int()

    @property
    def name(self) -> str:
        """Method name"""
        return _get_method_property(self.index, MethodProps.NAME).as_string()

    @property
    def description(self) -> Optional[str]:
        """Method description"""
        maybe_description = _get_method_property(self.index, MethodProps.NAME)
        if maybe_description.has_value:
            return maybe_description.as_string()
        return None

    @property
    def decoder(self) -> Optional[UUID]:
        """CLSID of decoder, if assigned."""
        decoder_is_assigned = _get_method_property(self.index, MethodProps.DECODER_IS_ASSIGNED).as_bool()
        if decoder_is_assigned:
            return _get_method_property(self.index, MethodProps.DECODER).as_uuid()
        return None

    @property
    def encoder(self) -> Optional[UUID]:
        """CLSID of encder, if assigned."""
        encoder_is_assigned = _get_method_property(self.index, MethodProps.ENCODER_IS_ASSIGNED).as_bool()
        if encoder_is_assigned:
            return _get_method_property(self.index, MethodProps.ENCODER).as_uuid()
        return None

    @property
    def num_streams(self) -> int:
        """Number of streams"""
        maybe_pack_streams = _get_method_property(self.index, MethodProps.PACK_STREAMS)
        if maybe_pack_streams.has_value:
            return maybe_pack_streams.as_int()
        return 1

    @property
    def is_filter(self) -> bool:
        """Method is a filter"""
        return _get_method_property(self.index, MethodProps.IS_FILTER).as_bool()


class MethodRegistry(Sequence):
    """
    Read-only access to 7-zip's archive format registry.
    """

    def __len__(self) -> int:
        return _get_num_methods()

    def __getitem__(self, index: int) -> MethodInfo:  # type: ignore
        if isinstance(index, int):
            return MethodInfo(index)
        raise TypeError()


methods = MethodRegistry()
