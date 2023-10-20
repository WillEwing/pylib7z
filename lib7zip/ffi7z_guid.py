#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uuid import UUID as GUID

from ._ffi7z import ffi, lib


def make7ZipIID(yy, xx):
    return GUID("{{23170F69-40C1-278A-0000-00{yy:s}00{xx:s}0000}}".format(xx=xx, yy=yy))


# IUnknown
IID_IUnknown = GUID("{00000000-0000-0000-C000-000000000046}")

# 00 IProgress.h
IID_IProgress = make7ZipIID("00", "05")

# 01 IFolderArchive.h
IID_IArchiveFolder = make7ZipIID("01", "05")
IID_IFolderArchiveExtractCallback = make7ZipIID("01", "07")
IID_IOutFolderArchive = make7ZipIID("01", "0A")
IID_IFolderArchiveUpdateCallback = make7ZipIID("01", "0B")
IID_IArchiveFolderInternal = make7ZipIID("01", "0C")
IID_IInFolderArchive = make7ZipIID("01", "0E")

# 03 IStream.h
IID_ISequentialInStream = make7ZipIID("03", "01")
IID_ISequentialOutStream = make7ZipIID("03", "02")
IID_IInStream = make7ZipIID("03", "03")
IID_IOutStream = make7ZipIID("03", "04")
IID_IStreamGetSize = make7ZipIID("03", "06")
IID_IOutStreamFlush = make7ZipIID("03", "07")

# 04 ICoder.h
IID_ICompressProgressInfo = make7ZipIID("04", "04")
IID_ICompressCoder = make7ZipIID("04", "05")
IID_ICompressCoder2 = make7ZipIID("04", "18")
IID_ICompressSetCoderProperties = make7ZipIID("04", "20")
IID_ICompressSetDecoderProperties2 = make7ZipIID("04", "22")
IID_ICompressWriteCoderProperties = make7ZipIID("04", "23")
IID_ICompressGetInStreamProcessedSize = make7ZipIID("04", "24")
IID_ICompressSetCoderMt = make7ZipIID("04", "25")
IID_ICompressGetSubStreamSize = make7ZipIID("04", "30")
IID_ICompressSetInStream = make7ZipIID("04", "31")
IID_ICompressSetOutStream = make7ZipIID("04", "32")
IID_ICompressSetInStreamSize = make7ZipIID("04", "33")
IID_ICompressSetOutStreamSize = make7ZipIID("04", "34")
IID_ICompressSetBufSize = make7ZipIID("04", "35")
IID_ICompressFilter = make7ZipIID("04", "40")
IID_ICompressCodecsInfo = make7ZipIID("04", "60")
IID_ISetCompressCodecsInfo = make7ZipIID("04", "61")
IID_ICryptoProperties = make7ZipIID("04", "80")
IID_ICryptoResetSalt = make7ZipIID("04", "88")
IID_ICryptoResetInitVector = make7ZipIID("04", "8C")
IID_ICryptoSetPassword = make7ZipIID("04", "90")
IID_ICryptoSetCRC = make7ZipIID("04", "A0")

# 05 IPassword.h
IID_ICryptoGetTextPassword = make7ZipIID("05", "10")
IID_ICryptoGetTextPassword2 = make7ZipIID("05", "11")

# 06 IArchive.h
IID_ISetProperties = make7ZipIID("06", "03")
IID_IArchiveOpenCallback = make7ZipIID("06", "10")
IID_IArchiveExtractCallback = make7ZipIID("06", "20")
IID_IArchiveOpenVolumeCallback = make7ZipIID("06", "30")
IID_IInArchiveGetStream = make7ZipIID("06", "40")
IID_IArchiveOpenSetSubArchiveName = make7ZipIID("06", "50")
IID_IInArchive = make7ZipIID("06", "60")
IID_IArchiveOpenSeq = make7ZipIID("06", "61")
IID_IArchiveUpdateCallback = make7ZipIID("06", "80")
IID_IArchiveUpdateCallback2 = make7ZipIID("06", "82")
IID_IOutArchive = make7ZipIID("06", "A0")

# 08 IFolder.h
IID_IFolderFolder = make7ZipIID("08", "00")
IID_IEnumProperties = make7ZipIID("08", "01")
IID_IFolderGetTypeID = make7ZipIID("08", "02")
IID_IFolderGetPath = make7ZipIID("08", "03")
IID_IFolderWasChanged = make7ZipIID("08", "04")
IID_IFolderOperations = make7ZipIID("08", "06")
IID_IFolderGetSystemIconIndex = make7ZipIID("08", "07")
IID_IFolderGetItemFullSize = make7ZipIID("08", "08")
IID_IFolderClone = make7ZipIID("08", "09")
IID_IFolderSetFlatMode = make7ZipIID("08", "0A")
IID_IFolderOperationsExtractCallback = make7ZipIID("08", "0B")
IID_IFolderProperties = make7ZipIID("08", "0E")
IID_IFolderArcProps = make7ZipIID("08", "10")
IID_IGetFolderArcProps = make7ZipIID("08", "11")


# Lookup

IIDS_BY_NAME = {
    "IArchiveExtractCallback": IID_IArchiveExtractCallback,
    "IArchiveOpenCallback": IID_IArchiveOpenCallback,
    "IArchiveOpenSetSubArchiveName": IID_IArchiveOpenSetSubArchiveName,
    "IArchiveOpenVolumeCallback": IID_IArchiveOpenVolumeCallback,
    "ICompressCodecsInfo": IID_ICompressCodecsInfo,
    "ICompressProgressInfo": IID_ICompressProgressInfo,
    "ICryptoGetTextPassword": IID_ICryptoGetTextPassword,
    "ICryptoGetTextPassword2": IID_ICryptoGetTextPassword2,
    "IInArchive": IID_IInArchive,
    "IInStream": IID_IInStream,
    "IOutStream": IID_IOutStream,
    "ISequentialInStream": IID_ISequentialInStream,
    "ISequentialOutStream": IID_ISequentialOutStream,
    "ISetCompressCodecsInfo": IID_ISetCompressCodecsInfo,
    "IUnknown": IID_IUnknown,
}

NAMES_BY_IID = {iid: name for name, iid in IIDS_BY_NAME.items()}


def get_iid_vtable_ptr(iid: GUID):
    "Get the virtual function table corresponding to the IID."
    name = f"FFI7Z_Py{NAMES_BY_IID[iid]}_vtable"
    vtable = getattr(lib, name)
    return ffi.addressof(vtable)


def get_iid_base_struct(iid: GUID):
    "Get the Python implementation struct corresponding to the IID."
    name = NAMES_BY_IID[iid]
    return f"FFI7Z_{name}"


def get_iid_impl_struct(iid: GUID):
    "Get the Python implementation struct corresponding to the IID."
    name = NAMES_BY_IID[iid]
    return f"FFI7Z_Py{name}"
