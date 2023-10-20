#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ._ffi7z import ffi, lib


@ffi.def_extern()
def FFI7Z_Py_IUnknown_QueryInterface(this, iid, out_object):
    this_struct = ffi.cast("FFI7Z_PyIUnknown *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.QueryInterface(iid, out_object)


@ffi.def_extern()
def FFI7Z_Py_IUnknown_AddRef(this):
    this_struct = ffi.cast("FFI7Z_PyIUnknown *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.AddRef()


@ffi.def_extern()
def FFI7Z_Py_IUnknown_Release(this):
    this_struct = ffi.cast("FFI7Z_PyIUnknown *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.Release()


@ffi.def_extern()
def FFI7Z_Py_ISequentialInStream_Read(this, data, size, processed_size):
    this_struct = ffi.cast("FFI7Z_PyISequentialInStream *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.Read(data, size, processed_size)


@ffi.def_extern()
def FFI7Z_Py_IInStream_Seek(this, offset, seekOrigin, newPosition):
    this_struct = ffi.cast("FFI7Z_PyIInStream *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.Seek(offset, seekOrigin, newPosition)


@ffi.def_extern()
def FFI7Z_Py_ISequentialOutStream_Write(this, data, size, processed_size):
    this_struct = ffi.cast("FFI7Z_PyISequentialOutStream *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.Write(data, size, processed_size)


@ffi.def_extern()
def FFI7Z_Py_IOutStream_Seek(this, offset, seekOrigin, newPosition):
    this_struct = ffi.cast("FFI7Z_PyIOutStream *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.Seek(offset, seekOrigin, newPosition)


@ffi.def_extern()
def FFI7Z_Py_IProgress_SetTotal(this, total):
    this_struct = ffi.cast("FFI7Z_PyIProgress *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.SetTotal(total)


@ffi.def_extern()
def FFI7Z_Py_IProgress_SetCompleted(this, complete_value):
    this_struct = ffi.cast("FFI7Z_PyIProgress *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.SetCompleted(complete_value)


@ffi.def_extern()
def FFI7Z_Py_IArchiveExtractCallback_GetStream(this, index, out_stream, ask_extract_mode):
    this_struct = ffi.cast("FFI7Z_PyIArchiveExtractCallback *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.GetStream(index, out_stream, ask_extract_mode)


@ffi.def_extern()
def FFI7Z_Py_IArchiveExtractCallback_PrepareOperation(this, ask_extract_mode):
    this_struct = ffi.cast("FFI7Z_PyIArchiveExtractCallback *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.PrepareOperation(ask_extract_mode)


@ffi.def_extern()
def FFI7Z_Py_IArchiveExtractCallback_SetOperationResult(this, op_result):
    this_struct = ffi.cast("FFI7Z_PyIArchiveExtractCallback *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.SetOperationResult(op_result)


@ffi.def_extern()
def FFI7Z_Py_IArchiveOpenCallback_SetTotal(this, files, bytes):
    this_struct = ffi.cast("FFI7Z_PyIArchiveOpenCallback *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.SetTotal(files, bytes)


@ffi.def_extern()
def FFI7Z_Py_IArchiveOpenCallback_SetCompleted(this, files, bytes):
    this_struct = ffi.cast("FFI7Z_PyIArchiveOpenCallback *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.SetCompleted(files, bytes)


@ffi.def_extern()
def FFI7Z_Py_IArchiveOpenSetSubArchiveName_SetSubArchiveName(this, name):
    this_struct = ffi.cast("FFI7Z_PyIArchiveOpenSetSubArchiveName *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.SetSubArchiveName(name)


@ffi.def_extern()
def FFI7Z_Py_IArchiveOpenVolumeCallback_GetProperty(this, prop_id, value):
    this_struct = ffi.cast("FFI7Z_PyIArchiveOpenVolumeCallback *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.GetProperty(prop_id, value)


@ffi.def_extern()
def FFI7Z_Py_IArchiveOpenVolumeCallback_GetStream(this, name, in_stream):
    this_struct = ffi.cast("FFI7Z_PyIArchiveOpenVolumeCallback *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.GetStream(name, in_stream)


@ffi.def_extern()
def FFI7Z_Py_ICompressProgressInfo_SetRatioInfo(this, in_size, out_size):
    this_struct = ffi.cast("FFI7Z_PyICompressProgressInfo *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.SetRatioInfo(in_size, out_size)


@ffi.def_extern()
def FFI7Z_Py_ICryptoGetTextPassword_CryptoGetTextPassword(this, password):
    this_struct = ffi.cast("FFI7Z_PyICryptoGetTextPassword *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.CryptoGetTextPassword(password)


@ffi.def_extern()
def FFI7Z_Py_ICryptoGetTextPassword2_CryptoGetTextPassword2(this, password_is_defined, password):
    this_struct = ffi.cast("FFI7Z_PyICryptoGetTextPassword2 *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.CryptoGetTextPassword2(password_is_defined, password)


@ffi.def_extern()
def FFI7Z_Py_IInArchive_Open(this, stream, max_check_start_position, open_callback):
    this_struct = ffi.cast("FFI7Z_PyIInArchive *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.Open(stream, max_check_start_position, open_callback)


@ffi.def_extern()
def FFI7Z_Py_IInArchive_Close(this):
    this_struct = ffi.cast("FFI7Z_PyIInArchive *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.Close()


@ffi.def_extern()
def FFI7Z_Py_IInArchive_GetNumberOfItems(this, num_items):
    this_struct = ffi.cast("FFI7Z_PyIInArchive *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.GetNumberOfItems(num_items)


@ffi.def_extern()
def FFI7Z_Py_IInArchive_GetProperty(this, index, prop_id, value):
    this_struct = ffi.cast("FFI7Z_PyIInArchive *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.GetProperty(index, prop_id, value)


@ffi.def_extern()
def FFI7Z_Py_IInArchive_Extract(this, indices, num_items, test_mode, extract_callback):
    this_struct = ffi.cast("FFI7Z_PyIInArchive *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.Extract(indices, num_items, test_mode, extract_callback)


@ffi.def_extern()
def FFI7Z_Py_IInArchive_GetArchiveProperty(this, prop_id, value):
    this_struct = ffi.cast("FFI7Z_PyIInArchive *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.GetArchiveProperty(prop_id, value)


@ffi.def_extern()
def FFI7Z_Py_IInArchive_GetNumberOfProperties(this, num_props):
    this_struct = ffi.cast("FFI7Z_PyIInArchive *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.GetNumberOfProperties(num_props)


@ffi.def_extern()
def FFI7Z_Py_IInArchive_GetPropertyInfo(this, index, name, prop_id, var_type):
    this_struct = ffi.cast("FFI7Z_PyIInArchive *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.GetPropertyInfo(index, name, prop_id, var_type)


@ffi.def_extern()
def FFI7Z_Py_IInArchive_GetNumberOfArchiveProperties(this, num_properties):
    this_struct = ffi.cast("FFI7Z_PyIInArchive *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.GetNumberOfArchiveProperties(num_properties)


@ffi.def_extern()
def FFI7Z_Py_IInArchive_GetArchivePropertyInfo(this, index, name, prop_id, var_type):
    this_struct = ffi.cast("FFI7Z_PyIInArchive *", this)
    self = ffi.from_handle(this_struct[0].pyobject_handle)
    return self.GetArchivePropertyInfo(index, name, prop_id, var_type)
