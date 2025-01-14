#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python base class for COM objects "PyUnknown"
"""

from logging import getLogger
from typing import Dict, Tuple
from uuid import UUID

from .ffi7z import ffi  # pylint: disable=no-name-in-module
from .hresult import HRESULT
from .iids import (
    NAMES_BY_IID,
    IID_IUnknown,
    iid_opaque_impl_struct_name,
    iid_python_impl_struct_name,
    iid_python_vtable_ptr,
    unmarshall_guid,
)

log = getLogger("lib7z")


class PyUnknown:
    """
    Base class for (7-zip) COM types in Python.
    """

    # pylint: disable=invalid-name

    IIDS: Tuple[UUID, ...]

    def __init__(self) -> None:
        self.refs = 1
        self.handle = ffi.new_handle(self)
        self.instances: Dict[UUID, ffi.CData] = {}
        for iid in {IID_IUnknown, *self.IIDS}:
            self.__make_instance(iid)

    def __make_instance(self, iid: UUID) -> None:
        impl_struct_name = iid_python_impl_struct_name(iid)
        instance = ffi.new(f"{impl_struct_name} *")
        instance[0].vtable = iid_python_vtable_ptr(iid)
        instance[0].self_handle = self.handle
        self.instances[iid] = instance

    def get_instance(self, iid: UUID) -> ffi.CData:
        """Get the interface struct corresponding to `idd`."""
        instance = self.instances[iid]
        return ffi.cast(f"{iid_opaque_impl_struct_name(iid)}*", instance)

    def QueryInterface(self, iid_ref, out_ref) -> HRESULT:
        """
        Try to get our instance of the interfaece specified by `iid_ref`.
        """
        iid = unmarshall_guid(iid_ref)
        try:
            instance = self.get_instance(iid)
            self.refs += 1
            out_ref[0] = instance
            return HRESULT.S_OK
        except KeyError:
            if iid not in NAMES_BY_IID:
                log.warning("QueryInterface: Unknown GUID {%s} from %s", iid, self.__class__.__name__)
            else:
                log.warning("QueryInterface: Requested %s from %s", NAMES_BY_IID[iid], self.__class__.__name__)
            out_ref[0] = ffi.NULL
            return HRESULT.E_NOINTERFACE

    def AddRef(self) -> int:
        """
        Increment the COM reference count.
        """
        self.refs += 1
        return self.refs

    def Release(self) -> int:
        """
        Decrement the COM reference count.
        """
        self.refs -= 1
        return self.refs
