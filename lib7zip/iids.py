#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
IIDs and IID lookup function.
"""

import sys
from uuid import UUID

from .ffi7zip import ffi, lib  # pylint: disable=no-name-in-module

# IIDs

IID_IUnknown = UUID("00000000-0000-0000-c000-000000000046")
IID_IProgress = UUID("23170f69-40c1-278a-0000-000000050000")
IID_IArchiveFolder = UUID("23170f69-40c1-278a-0000-000100050000")
IID_IFolderArchiveExtractCallback = UUID("23170f69-40c1-278a-0000-000100070000")
IID_IOutFolderArchive = UUID("23170f69-40c1-278a-0000-0001000a0000")
IID_IFolderArchiveUpdateCallback = UUID("23170f69-40c1-278a-0000-0001000b0000")
IID_IArchiveFolderInternal = UUID("23170f69-40c1-278a-0000-0001000c0000")
IID_IInFolderArchive = UUID("23170f69-40c1-278a-0000-0001000e0000")
IID_ISequentialInStream = UUID("23170f69-40c1-278a-0000-000300010000")
IID_ISequentialOutStream = UUID("23170f69-40c1-278a-0000-000300020000")
IID_IInStream = UUID("23170f69-40c1-278a-0000-000300030000")
IID_IOutStream = UUID("23170f69-40c1-278a-0000-000300040000")
IID_IStreamGetSize = UUID("23170f69-40c1-278a-0000-000300060000")
IID_IOutStreamFlush = UUID("23170f69-40c1-278a-0000-000300070000")
IID_ICompressProgressInfo = UUID("23170f69-40c1-278a-0000-000400040000")
IID_ICompressCoder = UUID("23170f69-40c1-278a-0000-000400050000")
IID_ICompressCoder2 = UUID("23170f69-40c1-278a-0000-000400180000")
IID_ICompressSetCoderProperties = UUID("23170f69-40c1-278a-0000-000400200000")
IID_ICompressSetDecoderProperties2 = UUID("23170f69-40c1-278a-0000-000400220000")
IID_ICompressWriteCoderProperties = UUID("23170f69-40c1-278a-0000-000400230000")
IID_ICompressGetInStreamProcessedSize = UUID("23170f69-40c1-278a-0000-000400240000")
IID_ICompressSetCoderMt = UUID("23170f69-40c1-278a-0000-000400250000")
IID_ICompressGetSubStreamSize = UUID("23170f69-40c1-278a-0000-000400300000")
IID_ICompressSetInStream = UUID("23170f69-40c1-278a-0000-000400310000")
IID_ICompressSetOutStream = UUID("23170f69-40c1-278a-0000-000400320000")
IID_ICompressSetInStreamSize = UUID("23170f69-40c1-278a-0000-000400330000")
IID_ICompressSetOutStreamSize = UUID("23170f69-40c1-278a-0000-000400340000")
IID_ICompressSetBufSize = UUID("23170f69-40c1-278a-0000-000400350000")
IID_ICompressFilter = UUID("23170f69-40c1-278a-0000-000400400000")
IID_ICompressCodecsInfo = UUID("23170f69-40c1-278a-0000-000400600000")
IID_ISetCompressCodecsInfo = UUID("23170f69-40c1-278a-0000-000400610000")
IID_ICryptoProperties = UUID("23170f69-40c1-278a-0000-000400800000")
IID_ICryptoResetSalt = UUID("23170f69-40c1-278a-0000-000400880000")
IID_ICryptoResetInitVector = UUID("23170f69-40c1-278a-0000-0004008c0000")
IID_ICryptoSetPassword = UUID("23170f69-40c1-278a-0000-000400900000")
IID_ICryptoSetCRC = UUID("23170f69-40c1-278a-0000-000400a00000")
IID_ICryptoGetTextPassword = UUID("23170f69-40c1-278a-0000-000500100000")
IID_ICryptoGetTextPassword2 = UUID("23170f69-40c1-278a-0000-000500110000")
IID_ISetProperties = UUID("23170f69-40c1-278a-0000-000600030000")
IID_IArchiveOpenCallback = UUID("23170f69-40c1-278a-0000-000600100000")
IID_IArchiveExtractCallback = UUID("23170f69-40c1-278a-0000-000600200000")
IID_IArchiveOpenVolumeCallback = UUID("23170f69-40c1-278a-0000-000600300000")
IID_IInArchiveGetStream = UUID("23170f69-40c1-278a-0000-000600400000")
IID_IArchiveOpenSetSubArchiveName = UUID("23170f69-40c1-278a-0000-000600500000")
IID_IInArchive = UUID("23170f69-40c1-278a-0000-000600600000")
IID_IArchiveOpenSeq = UUID("23170f69-40c1-278a-0000-000600610000")
IID_IArchiveUpdateCallback = UUID("23170f69-40c1-278a-0000-000600800000")
IID_IArchiveUpdateCallback2 = UUID("23170f69-40c1-278a-0000-000600820000")
IID_IOutArchive = UUID("23170f69-40c1-278a-0000-000600a00000")
IID_IFolderFolder = UUID("23170f69-40c1-278a-0000-000800000000")
IID_IEnumProperties = UUID("23170f69-40c1-278a-0000-000800010000")
IID_IFolderGetTypeID = UUID("23170f69-40c1-278a-0000-000800020000")
IID_IFolderGetPath = UUID("23170f69-40c1-278a-0000-000800030000")
IID_IFolderWasChanged = UUID("23170f69-40c1-278a-0000-000800040000")
IID_IFolderOperations = UUID("23170f69-40c1-278a-0000-000800060000")
IID_IFolderGetSystemIconIndex = UUID("23170f69-40c1-278a-0000-000800070000")
IID_IFolderGetItemFullSize = UUID("23170f69-40c1-278a-0000-000800080000")
IID_IFolderClone = UUID("23170f69-40c1-278a-0000-000800090000")
IID_IFolderSetFlatMode = UUID("23170f69-40c1-278a-0000-0008000a0000")
IID_IFolderOperationsExtractCallback = UUID("23170f69-40c1-278a-0000-0008000b0000")
IID_IFolderProperties = UUID("23170f69-40c1-278a-0000-0008000e0000")
IID_IFolderArcProps = UUID("23170f69-40c1-278a-0000-000800100000")
IID_IGetFolderArcProps = UUID("23170f69-40c1-278a-0000-000800110000")

# Lookup helpers

# TODO: There is almost certainly a better way to do this. Find it.
IIDS_BY_NAME = {name[4:]: value for name, value in sys.modules[__name__].__dict__ if name.startswith("IID_")}
NAMES_BY_IID = {value: name for name, value in IIDS_BY_NAME}


def iid_opaque_impl_struct_name(iid: UUID) -> str:
    """Get the name of the opaque implemtation struct corresponding to `iid`."""
    name = NAMES_BY_IID[iid]
    return f"FFI7Z_{name}"


def iid_python_impl_struct_name(iid: UUID) -> str:
    """Get the name of the python implemtation struct corresponding to `iid`."""
    name = NAMES_BY_IID[iid]
    return f"FFI7Z_Py{name}"


def iid_python_vtable_ptr(iid: UUID) -> ffi.CData:
    """Get a pointer to the python thunk vtable corresponding to `iid`."""
    interface_name = NAMES_BY_IID[iid]
    vtable_name = f"FFI7Z_Py{interface_name}_vtable"
    vtable = getattr(lib, vtable_name)
    return ffi.addressof(vtable)
