# -*- coding: utf-8 -*-
"""
Python bindings to the 7-Zip Library
"""

__author__ = "Mark Harviston, William Ewing"
__license__ = "BSD"
__version__ = "0.1.1"

from uuid import UUID as GUID
from collections import namedtuple
from dataclasses import dataclass
from functools import partial
import os.path
import sys

import logging

log = logging.getLogger(__name__)
if os.environ.get("DEBUG"):
    logging.basicConfig(level=logging.DEBUG)
    log.debug("begin")


from ctypes.util import find_library, find_msvcrt
from cffi import FFI

ffi = FFI()

from . import wintypes, py7ziptypes, comtypes
from .wintypes import VARTYPE
from .py7ziptypes import FormatProps, MethodProps

ffi.cdef(wintypes.CDEFS)
ffi.cdef(comtypes.CDEFS)
ffi.cdef(py7ziptypes.CDEFS)

ffi.cdef(
    """

HRESULT GetMethodProperty(uint32_t index, PROPID propID, PROPVARIANT * value);
HRESULT GetNumberOfMethods(uint32_t * numMethods);
HRESULT GetNumberOfFormats(uint32_t * numFormats);
HRESULT GetHandlerProperty(PROPID propID, PROPVARIANT * value); /* Unused */
HRESULT GetHandlerProperty2(uint32_t index, PROPID propID, PROPVARIANT * value);
HRESULT CreateObject(const GUID * clsID, const GUID * iid, void ** outObject);
HRESULT SetLargePageMode(); /* Unused */

void* calloc(size_t, size_t);
void* malloc(size_t);
void* memset(void*, int, size_t);
void free(void*);


"""
)

# initalize/path detection
env_path = os.environ.get("7ZDLL_PATH")
dll_paths = [env_path] if env_path else []

if "win" in sys.platform:
    try:
        log.info("Detecting 7z.dll path from registry")
        from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE, KEY_READ

        aKey = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\7-Zip", 0, KEY_READ)
        s7z_path = QueryValueEx(aKey, "Path")[0]
        dll_paths.append(os.path.join(s7z_path, "7z.dll"))
    except WinError:
        log.warn("Could not find 7-zip installation info in registry.")

    if not dll_paths:
        log.info("Searching for 7z.dll in default search path.")
        maybe_lib7z_path = find_library("7z")
        if maybe_lib7z_path:
            dll_paths.append(maybe_lib7z_path)

    ole32 = ffi.dlopen("ole32")
    free_propvariant = lambda x: ole32.PropVariantClear(x)

    # NOTE: Apparently, Python doesn't know what msvcrt it's using sometimes?
    libc_path = find_msvcrt() or find_library("ucrtbase")
else:

    def free_propvariant(void_p):
        # TODO make smarter
        pvar = ffi.cast("PROPVARIANT*", void_p)
        if pvar.vt == wintypes.VT_BSTR and pvar.bstrVal != ffi.NULL:
            C.free(pvar.bstrVal)

        C.memset(pvar, 0, ffi.sizeof("PROPVARIANT"))

    suffixes = "", "7z.so", "p7zip/7z.so"
    prefixes = ["/lib", "/usr/lib"]
    for suffix in suffixes:
        for prefix in prefixes:
            dll_paths.append(os.path.join(prefix, suffix))

    libc_path = find_library("c")

log.info("dll_paths: %r", dll_paths)
dll7z = None
for dll_path in dll_paths:
    log.debug("trying path: %s", dll_path)
    try:
        dll7z = ffi.dlopen(dll_path)
    except:
        dll7z = None
    else:
        break


if dll7z is None:
    raise Exception("Could not find 7z.dll/7z.so")

C = ffi.dlopen(libc_path)

from .winhelpers import get_prop_val, guidp2uuid, alloc_propvariant, RNOK


def get_prop(idx, propid, get_fn, prop_name, convert, istype=None):
    log.debug("get_prop(%d, %d, -, -, istype=%d)", idx, propid, istype)

    # if propid == MethodProps.kID and getting_meths:
    # 	import pdb; pdb.set_trace()

    tmp_pvar = alloc_propvariant()
    as_pvar = ffi.cast("PROPVARIANT*", tmp_pvar)
    log.debug("getting prop value")
    RNOK(get_fn(idx, propid, as_pvar))
    if as_pvar == ffi.NULL:
        log.debug("pvar == NULL")
        return None
    elif as_pvar.vt in (VARTYPE.VT_EMPTY, VARTYPE.VT_NULL):
        log.debug("vt == VT_NULL or VT_EMPTY")
        return None
    elif istype is not None:
        vt = VARTYPE(as_pvar.vt)
        log.debug("vt: %r", vt)
        assert vt == istype

    val = getattr(as_pvar, prop_name)

    if as_pvar.vt in (VARTYPE.VT_CLSID, VARTYPE.VT_BSTR):
        if val == ffi.NULL:
            log.debug("pointer NULL")
            return None

    return convert(val)


get_bytes_prop = partial(get_prop, prop_name="pcVal", istype=VARTYPE.VT_BSTR, convert=ffi.string)
get_string_prop = partial(get_prop, prop_name="bstrVal", istype=VARTYPE.VT_BSTR, convert=ffi.string)
get_classid = partial(get_prop, prop_name="puuid", istype=VARTYPE.VT_BSTR, convert=guidp2uuid)
get_hex_prop = partial(get_prop, prop_name="ulVal", istype=VARTYPE.VT_UI4, convert=lambda x: hex(int(x)))
get_bool_prop = partial(get_prop, prop_name="bVal", istype=VARTYPE.VT_BOOL, convert=lambda x: x != 0)
get_uint64_prop = partial(get_prop, prop_name="uhVal", istype=VARTYPE.VT_UI8, convert=int)
get_uint32_prop = partial(get_prop, prop_name="ulVal", istype=VARTYPE.VT_UI4, convert=lambda x: x)


@dataclass
class Format:
    name: str
    index: int
    classid: GUID
    extensions: tuple[str]
    start_signature: bytes


def get_format_info(format_idx):
    extensions_raw = get_string_prop(format_idx, FormatProps.kExtension, dll7z.GetHandlerProperty2)
    extensions = tuple(extensions_raw.split())
    return Format(
        name=get_string_prop(format_idx, FormatProps.kName, dll7z.GetHandlerProperty2),
        index=format_idx,
        classid=get_classid(format_idx, FormatProps.kClassID, dll7z.GetHandlerProperty2),
        extensions=extensions,
        start_signature=get_bytes_prop(format_idx, FormatProps.kStartSignature, dll7z.GetHandlerProperty2),
    )


def get_num_formats() -> int:
    num_formats_ptr = ffi.new("uint32_t[1]", [0])
    RNOK(dll7z.GetNumberOfFormats(num_formats_ptr))
    return num_formats_ptr[0]


def get_formats():
    num_formats = get_num_formats()
    return {fmt.name: fmt for fmt in (get_format_info(n) for n in range(num_formats))}


Method = namedtuple("Method", ("name", "id", "encoder", "decoder", "encoder_assigned", "decoder_assigned"))


def get_method_info():
    log.debug("getting methods")
    num_methods = ffi.new("uint32_t*")
    RNOK(dll7z.GetNumberOfMethods(num_methods))
    assert num_methods != ffi.NULL
    log.debug("num_methods=%d", int(num_methods[0]))
    method_info = [
        Method(
            get_string_prop(i, MethodProps.kName, dll7z.GetMethodProperty),
            get_uint64_prop(i, MethodProps.kID, dll7z.GetMethodProperty),
            get_classid(i, MethodProps.kEncoder, dll7z.GetMethodProperty),
            get_classid(i, MethodProps.kDecoder, dll7z.GetMethodProperty),
            get_bool_prop(i, MethodProps.kEncoderIsAssigned, dll7z.GetMethodProperty),
            get_bool_prop(i, MethodProps.kDecoderIsAssigned, dll7z.GetMethodProperty),
        )
        for i in range(num_methods[0])
    ]
    log.debug("got method info")
    return method_info


getting_meths = False
log.debug("initializing")
formats = get_formats()
max_sig_size = max((len(f.start_signature) for f in formats.values() if f.start_signature is not None))
getting_meths = True
methods = get_method_info()

"""
from pprint import pprint
from functools import partial
pp = partial(pprint, indent=True)
pp(methods)
"""

from .archive import Archive  # noqa
