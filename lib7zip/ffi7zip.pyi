"""
Python Bindings for 7-zip: C-Python FFI bridge.
"""

from cffi.api import FFI

class Lib:
    # Memory allocation
    def CreatePropVariant(self) -> FFI.CData: ...
    def DeletePropVariant(self, prop_var: FFI.CData) -> None: ...
    # 7z.dll components
    def InitModule(self, lib7zip_path: FFI.CData) -> FFI.CData: ...
    def CreateObject(self, clsid: FFI.CData, iid: FFI.CData, out_object: FFI.CData) -> FFI.CData: ...
    def GetNumberOfFormats(self, num_formats: FFI.CData) -> FFI.CData: ...
    def GetHandlerProperty2(self, index: FFI.CData, prop_id: FFI.CData, prop_var: FFI.CData) -> FFI.CData: ...
    def GetNumberOfMethods(self, num_methods: FFI.CData) -> FFI.CData: ...
    def GetMethodProperty(self, index: FFI.CData, prop_id: FFI.CData, prop_var: FFI.CData) -> FFI.CData: ...


ffi: FFI
lib: Lib