#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ._ffi7z import ffi, lib
from .ffi7z_guid import *
from .ffi7z_thunk import *
from .ffi7z_types import *


def __load_lib7z():
    library_path = "F:\\Bethesda Game Mods\\ModCurator\\.venv\\Sripts\\7z.dll"
    try:
        from winreg import HKEY_LOCAL_MACHINE, KEY_READ, OpenKey, QueryValueEx

        key = OpenKey(HKEY_LOCAL_MACHINE, "SOFTWARE\\7-zip", 0, KEY_READ)
        library_path = QueryValueEx(key, "Path")[0] + "\\7z.dll"
    except WindowsError:
        pass

    result = HRESULT(lib.InitModule(library_path))
    if result != HRESULT.S_OK:
        raise RuntimeError("Could not open 7-Zip Library.")

    print("Loaded 7z.dll")


ffi.init_once(__load_lib7z, "load_lib7z")


def MarshallGUID(guid: GUID) -> ffi.CData:
    result = ffi.new("GUID *")
    ffi.buffer(result, 16)[:] = guid.bytes_le
    return result


def UnmarshallGUID(pguid: ffi.CData) -> GUID:
    return GUID(bytes_le=ffi.buffer(pguid, 16)[:])


def CreatePropVariant() -> ffi.CData:
    "Create a PROPVARIANT."
    return ffi.gc(lib.CreatePropVariant(), lib.DeletePropVariant)


def ReleaseObject(obj):
    if obj == ffi.NULL:
        return
    obj.vtable.Release(obj)


def CreateObject(clsid: GUID, iid: GUID) -> ffi.CData:
    "Create an Object of the specified class and interface id."
    created_object_ptr = ffi.new("void **")
    result = HRESULT(lib.CreateObject(MarshallGUID(clsid), MarshallGUID(iid), created_object_ptr))
    if result != HRESULT.S_OK:
        raise RuntimeError("Failed to create object (clsid:%r,iid:%r): %s", clsid, iid, result)
    created_object = ffi.cast("FFI7Z_IUnknown *", created_object_ptr[0])
    return ffi.gc(created_object, ReleaseObject)


def UnwrapPropGUID(pvar):
    "Unwrap a PROPVARIANT-wrapped GUID."
    vt = VARTYPE(pvar.vt)
    if vt != VARTYPE.VT_BSTR:
        return PropUnwrapError(vt)
    return UnmarshallGUID(pvar.bstrVal)


def UnwrapPropBytesZ(pvar):
    "Unwrap a PROPVARIANT-wrapped null-terminated bytesting."
    vt = VARTYPE(pvar.vt)
    if vt != VARTYPE.VT_BSTR:
        raise PropUnwrapError(vt)
    return ffi.string(pvar.pszVal)


def UnwrapPropMultiSig(pvar):
    vt = VARTYPE(pvar.vt)
    if vt != VARTYPE.VT_BSTR:
        raise PropUnwrapError(vt)

    offset = 0
    packed = pvar.pszVal
    signatures = []

    while ord(packed[offset]) != 0:
        size = ord(packed[offset])
        next_offset = offset + size + 1
        signatures.append(ffi.unpack(packed[offset:next_offset], size))
        offset = next_offset

    return tuple(signatures)


def GetMethodProperty(index, prop_id, unwrap_func=UnwrapPropAuto):
    pvar = CreatePropVariant()
    result = HRESULT(lib.GetMethodProperty(index, prop_id, pvar))
    if result != HRESULT.S_OK:
        raise RuntimeError("Could not get property %r from method %r: %s", prop_id, index, result)
    return unwrap_func(pvar)


def GetNumberOfMethods() -> int:
    num_methods = ffi.new("uint32_t *", 0)
    result = HRESULT(lib.GetNumberOfMethods(num_methods))
    if result != HRESULT.S_OK:
        raise RuntimeError(result.desc)
    return num_methods[0]


def GetFormatProperty(index, prop_id, unwrap_func=UnwrapPropAuto):
    pvar = CreatePropVariant()
    result = HRESULT(lib.GetHandlerProperty2(index, prop_id, pvar))
    if result != HRESULT.S_OK:
        raise RuntimeError("Could not get property %r from method %r: %s", prop_id, index, result)
    return unwrap_func(pvar)


def GetNumberOfFormats() -> int:
    num_formats = ffi.new("uint32_t *", 0)
    result = HRESULT(lib.GetNumberOfFormats(num_formats))
    if result != HRESULT.S_OK:
        raise RuntimeError(result.desc)
    return num_formats[0]


class IUnknownImpl:
    "Implementation of 7-zip COM IUnknown interface."

    def __init__(self) -> None:
        self.refs = 1
        self.instances_ref = {}
        self.instances = {}
        self.handle = ffi.new_handle(self)
        for iid in {IID_IUnknown, *self.IIDS}:
            self.__make_instance(iid)

    def __make_instance(self, iid: GUID):
        instance_type = get_iid_impl_struct(iid)
        instance = ffi.new(f"{instance_type} *")
        instance[0].vtable = get_iid_vtable_ptr(iid)
        instance[0].pyobject_handle = self.handle
        self.instances_ref[iid] = instance
        instance_base_type = get_iid_base_struct(iid)
        self.instances[iid] = ffi.cast(f"{instance_base_type} *", instance)

    def QueryInterface(self, iid_ref, out_ref) -> int:
        self.refs += 1
        iid = UnmarshallGUID(iid_ref)
        if iid in self.instances:
            out_ref[0] = self.instances[iid]
            return int(HRESULT.S_OK)
        else:
            out_ref[0] = ffi.NULL
            return int(HRESULT.E_NOINTERFACE)

    def AddRef(self) -> int:
        self.refs += 1
        return self.refs

    def Release(self) -> int:
        self.refs -= 1
        return self.refs
