#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import UTC, datetime, timedelta
from enum import IntEnum

from ._ffi7z import ffi, lib


class HRESULT(IntEnum):
    S_OK = 0x00000000  # Operation successful
    S_FALSE = -1  # Generic Error
    E_ABORT = 0x80004004  # Operation aborted
    E_ACCESSDENIED = 0x80070005  # General access denied error
    E_FAIL = 0x80004005  # Unspecified failure
    E_HANDLE = 0x80070006  # Handle that is not valid
    E_INVALIDARG = 0x80070057  # One or more arguments are not valid
    E_NOINTERFACE = 0x80004002  # No such interface supported
    E_NOTIMPL = 0x80004001  # Not implemented
    E_OUTOFMEMORY = 0x8007000E  # Failed to allocate necessary memory
    E_POINTER = 0x80004003  # Pointer that is not valid
    E_UNEXPECTED = 0x8000FFFF  # Unexpected failure

    @property
    def desc(self):
        descriptions = {
            HRESULT.S_OK: "Operation Successful",
            HRESULT.E_ABORT: "Operation Aborted",
            HRESULT.E_ACCESSDENIED: "General Access Denied Error",
            HRESULT.E_FAIL: "Unspecified Failure",
            HRESULT.E_HANDLE: "Handle that is not valid",
            HRESULT.E_INVALIDARG: "One or more arguments are not valid",
            HRESULT.E_NOINTERFACE: "No such interface supported",
            HRESULT.E_NOTIMPL: "Not implemented",
            HRESULT.E_OUTOFMEMORY: "Failed to allocate necessary memory",
            HRESULT.E_POINTER: "Pointer that is not valid",
            HRESULT.E_UNEXPECTED: "Unexpected failure",
        }

        try:
            return descriptions[self]
        except KeyError:
            return "Unknown Error Code"


class VARTYPE(IntEnum):
    VT_EMPTY = 0
    VT_NULL = 1
    VT_I2 = 2
    VT_I4 = 3
    VT_R4 = 4
    VT_R8 = 5
    VT_CY = 6
    VT_DATE = 7
    VT_BSTR = 8
    VT_DISPATCH = 9
    VT_ERROR = 10
    VT_BOOL = 11
    VT_VARIANT = 12
    VT_UNKNOWN = 13
    VT_DECIMAL = 14
    VT_I1 = 16
    VT_UI1 = 17
    VT_UI2 = 18
    VT_UI4 = 19
    VT_I8 = 20
    VT_UI8 = 21
    VT_INT = 22
    VT_UINT = 23
    VT_VOID = 24
    VT_HRESULT = 25
    VT_FILETIME = 64


class FormatProps(IntEnum):
    kName = 0  # str
    kClassID = 1  # str or GID
    kExtension = 2  # str
    kAddExtension = 3  # str
    kUpdate = 4  # bool
    kKeepName = 5  # bool
    kSignature = 6  # bytes or str
    kMultiSignature = 7  # bytes or str
    kSignatureOffset = 8  # uint32_t
    kAltStreams = 9  # bool
    kNtSecure = 10  # bool
    kFlags = 11  # uint32_t
    kTimeFlags = 12  # uint32_t


class MethodProps(IntEnum):
    kID = 0
    kName = 1
    kDecoder = 2
    kEncoder = 3
    kInStreams = 4
    kOutStreams = 5
    kDescription = 6
    kDecoderIsAssigned = 7
    kEncoderIsAssigned = 8


class ArchiveProps(IntEnum):
    """Archive and Archive Item Propertys"""

    NO_PROPERTY = 0  # kpidNoProperty
    MAIN_SUBFILE = 1  # kpidMainSubfile
    HANDLER_ITEM_INDEX = 2  # kpidHandlerItemIndex
    PATH = 3  # kpidPath
    NAME = 4  # kpidName
    EXTENSION = 5  # kpidExtension
    IS_DIR = 6  # kpidIsDir
    SIZE = 7  # kpidSize
    PACK_SIZE = 8  # kpidPackSize
    ATTRIB = 9  # kpidAttrib
    CTIME = 10  # kpidCTime
    ATIME = 11  # kpidATime
    MTIME = 12  # kpidMTime
    SOLID = 13  # kpidSolid
    COMMENTED = 14  # kpidCommented
    ENCRYPTED = 15  # kpidEncrypted
    SPLIT_BEFORE = 16  # kpidSplitBefore
    SPLIT_AFTER = 17  # kpidSplitAfter
    DICTIONARY_SIZE = 18  # kpidDictionarySize
    CRC = 19  # kpidCRC
    TYPE = 20  # kpidType
    IS_ANTI = 21  # kpidIsAnti
    METHOD = 22  # kpidMethod
    HOST_OS = 23  # kpidHostOS
    FILE_SYSTEM = 24  # kpidFileSystem
    USER = 25  # kpidUser
    GROUP = 26  # kpidGroup
    BLOCK = 27  # kpidBlock
    COMMENT = 28  # kpidComment
    POSITION = 29  # kpidPosition
    PREFIX = 30  # kpidPrefix
    NUM_SUB_DIRS = 31  # kpidNumSubDirs
    NUM_SUB_FILES = 32  # kpidNumSubFiles
    UNPACK_VER = 33  # kpidUnpackVer
    VOLUME = 34  # kpidVolume
    IS_VOLUME = 35  # kpidIsVolume
    OFFSET = 36  # kpidOffset
    LINKS = 37  # kpidLinks
    NUM_BLOCKS = 38  # kpidNumBlocks
    NUM_VOLUMES = 39  # kpidNumVolumes
    TIME_TYPE = 40  # kpidTimeType
    BIT64 = 41  # kpidBit64
    BIG_ENDIAN = 42  # kpidBigEndian
    CPU = 43  # kpidCpu
    PHY_SIZE = 44  # kpidPhySize
    HEADERS_SIZE = 45  # kpidHeadersSize
    CHECKSUM = 46  # kpidChecksum
    CHARACTS = 47  # kpidCharacts
    VA = 48  # kpidVa
    ID = 49  # kpidId
    SHORT_NAME = 50  # kpidShortName
    CREATOR_APP = 51  # kpidCreatorApp
    SECTOR_SIZE = 52  # kpidSectorSize
    POSIX_ATTRIB = 53  # kpidPosixAttrib
    SYMLINK = 54  # kpidSymLink
    ERROR = 55  # kpidError
    TOTAL_SIZE = 56  # kpidTotalSize
    FREE_SPACE = 57  # kpidFreeSpace
    CLUSTER_SIZE = 58  # kpidClusterSize
    VOLUME_NAME = 59  # kpidVolumeName
    LOCAL_NAME = 60  # kpidLocalName
    PROVIDER = 61  # kpidProvider
    NT_SECURE = 62  # kpidNtSecure
    IS_ALT_STREAM = 63  # kpidIsAltStream
    IS_AUX = 64  # kpidIsAux
    IS_DELETED = 65  # kpidIsDeleted
    IS_TREE = 66  # kpidIsTree
    SHA1 = 67  # kpidSha1
    SHA256 = 68  # kpidSha256
    ERROR_TYPE = 69  # kpidErrorType
    NUM_ERRORS = 70  # kpidNumErrors
    ERROR_FLAGS = 71  # kpidErrorFlags
    WARNING_FLAGS = 72  # kpidWarningFlags
    WARNING = 73  # kpidWarning
    NUM_STREAMS = 74  # kpidNumStreams
    NUM_ALT_STREAMS = 75  # kpidNumAltStreams
    ALT_STREAMS_SIZE = 76  # kpidAltStreamsSize
    VIRTUAL_SIZE = 77  # kpidVirtualSize
    UNPACK_SIZE = 78  # kpidUnpackSize
    TOTAL_PHY_SIZE = 79  # kpidTotalPhySize
    VOLUME_INDEX = 80  # kpidVolumeIndex
    SUB_TYPE = 81  # kpidSubType
    SHORT_COMMENT = 82  # kpidShortComment
    CODE_PAGE = 83  # kpidCodePage
    IS_NOT_ARC_TYPE = 84  # kpidIsNotArcType
    PHY_SIZE_CANT_BE_DETECTED = 85  # kpidPhySizeCantBeDetected
    ZEROS_TAIL_IS_ALLOWED = 86  # kpidZerosTailIsAllowed
    TAIL_SIZE = 87  # kpidTailSize
    EMBEDDED_STUB_SIZE = 88  # kpidEmbeddedStubSize
    NT_REPARSE = 89  # kpidNtReparse
    HARD_LINK = 90  # kpidHardLink
    INODE = 91  # kpidINode
    STREAM_ID = 92  # kpidStreamId
    READ_ONLY = 93  # kpidReadOnly
    OUT_NAME = 94  # kpidOutName
    COPY_LINK = 95  # kpidCopyLink
    ARC_FILE_NAME = 96  # kpidArcFileName
    IS_HASH = 97  # kpidIsHash
    CHANGE_TIME = 98  # kpidChangeTime
    USER_ID = 99  # kpidUserId
    GROUP_ID = 100  # kpidGroupId
    DEVICE_MAJOR = 101  # kpidDeviceMajor
    DEVICE_MINOR = 102  # kpidDeviceMinor
    DEV_MAJOR = 103  # kpidDevMajor
    DEV_MINOR = 104  # kpidDevMinor

    USER_DEFINED = 0x10000  # kpidUserDefined


class OperationResult(IntEnum):
    kOK = 0
    kUnSupportedMethod = 1
    kDataError = 2
    kCRCError = 3


class AskMode(IntEnum):
    kExtract = 0
    kTest = 1
    kSkip = 2


VT_DATE_ZERO = datetime(year=1899, month=12, day=31, tzinfo=UTC)
VT_FILETIME_ZERO = datetime(year=1601, month=1, day=1, tzinfo=UTC)


class PropUnwrapError(RuntimeError):
    pass


def UnwrapPropAuto(pvar):
    vt = VARTYPE(pvar.vt)
    if vt == VARTYPE.VT_EMPTY:
        raise PropUnwrapError(vt)
    if vt == VARTYPE.VT_NULL:
        return None
    if vt == VARTYPE.VT_I2:
        return int(pvar.iVal)
    if vt == VARTYPE.VT_I4:
        return int(pvar.lVal)
    if vt == VARTYPE.VT_R4:
        return float(pvar.fltVal)
    if vt == VARTYPE.VT_R8:
        return float(pvar.dblVal)
    if vt == VARTYPE.VT_CY:
        raise NotImplementedError(vt)
    if vt == VARTYPE.VT_DATE:
        return VT_DATE_ZERO + timedelta(days=float(pvar.dblVal))
    if vt == VARTYPE.VT_BSTR:
        return ffi.string(pvar.bstrVal)
    if vt == VARTYPE.VT_DISPATCH:
        raise NotImplementedError(vt)
    if vt == VARTYPE.VT_ERROR:
        raise NotImplementedError(vt)
    if vt == VARTYPE.VT_BOOL:
        return bool(pvar.boolVal)
    if vt == VARTYPE.VT_VARIANT:
        raise NotImplementedError(vt)
    if vt == VARTYPE.VT_UNKNOWN:
        raise NotImplementedError(vt)
    if vt == VARTYPE.VT_DECIMAL:
        raise NotImplementedError(vt)
    if vt == VARTYPE.VT_I1:
        return int(pvar.cVal)
    if vt == VARTYPE.VT_UI1:
        return int(pvar.bVal)
    if vt == VARTYPE.VT_UI2:
        return int(pvar.uiVal)
    if vt == VARTYPE.VT_UI4:
        return int(pvar.ulVal)
    if vt == VARTYPE.VT_I8:
        return int(pvar.hVal.QuadPart)
    if vt == VARTYPE.VT_UI8:
        return int(pvar.uhVal.QuadPart)
    if vt == VARTYPE.VT_INT:
        return int(pvar.intVal)
    if vt == VARTYPE.VT_UINT:
        return int(pvar.uintVar)
    if vt == VARTYPE.VT_VOID:
        raise NotImplementedError(vt)
    if vt == VARTYPE.VT_HRESULT:
        return HRESULT(vt.ulVal)
    if vt == VARTYPE.FILETIME:
        return VT_FILETIME_ZERO + timedelta(microseconds=int(vt.uhVal.QuadPart))
    raise NotImplementedError(vt)
