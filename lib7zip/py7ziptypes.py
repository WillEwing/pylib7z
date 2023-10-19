# -*- coding: utf-8 -*-
import uuid
from enum import Enum, IntEnum
from string import Template

from .comtypes import CDEF_IUnknown

CDEFS = Template(
    """
typedef uint32_t PROPID; /*actually an enum, often a different enum for each function...*/

typedef struct {
	$CDEF_IUnknown
	/* Inherited from ISequentialInstream */
	HRESULT (*Read)(void* self, uint8_t *data, uint32_t size, uint32_t *processedSize);
	/* Own methods */
	HRESULT (*Seek)(void* self, int64_t offset, uint32_t seekOrigin, uint64_t *newPosition);
} _IInStream_vtable;

typedef struct{
	_IInStream_vtable* vtable;
} IInStream;

typedef struct {
	$CDEF_IUnknown
	HRESULT (*Write)(void* self, const void *data, uint32_t size, uint32_t *processedSize);
	/*
	if (size > 0) this function must write at least 1 byte.
	This function is allowed to write less than "size".
	You must call Write function in loop, if you need to write exact amount of data
	*/
	HRESULT (*Seek)(void* self, int64_t offset, uint32_t seekOrigin, uint64_t *newPosition);
} _IOutStream_vtable;

typedef struct {
	_IOutStream_vtable* vtable;
} IOutStream;

typedef IOutStream ISequentialOutStream;
typedef _IOutStream_vtable _ISequentialOutStream_vtable;
typedef IInStream ISequentialInStream;
typedef _IInStream_vtable _ISequentialInStream_vtable;

typedef struct {
	$CDEF_IUnknown
	HRESULT(*SetTotal)(void* self, const uint64_t *files, const uint64_t *bytes);
	HRESULT(*SetCompleted)(void* self, const uint64_t *files, const uint64_t *bytes);
} _IArchiveOpenCallback_vtable;

typedef struct {
	_IArchiveOpenCallback_vtable* vtable;
} IArchiveOpenCallback;

typedef struct {
	$CDEF_IUnknown
	HRESULT(*SetTotal)(void* self, uint64_t total);
	HRESULT(*SetCompleted)(void* self, const uint64_t *completeValue);
	HRESULT(*GetStream)(void* self, uint32_t index, ISequentialOutStream **outStream,  int32_t askExtractMode);
	HRESULT(*PrepareOperation)(void* self, int32_t askExtractMode);
	HRESULT(*SetOperationResult)(void* self, int32_t resultEOperationResult);
} _IArchiveExtractCallback_vtable;

typedef struct {_IArchiveExtractCallback_vtable* vtable; } IArchiveExtractCallback;

typedef struct {
	$CDEF_IUnknown
	HRESULT(*SetRatioInfo)(void* self, const uint64_t *inSize, const uint64_t *outSize);
} _ICompressProgressInfo_vtable;
typedef struct {_ICompressProgressInfo_vtable* vtable;} ICompressProgressInfo;

typedef struct {
	$CDEF_IUnknown
	HRESULT (*Open)(void* self, IInStream *stream, const uint64_t *maxCheckStartPosition, IArchiveOpenCallback *openArchiveCallback);
	HRESULT (*Close)(void* self);
	HRESULT (*GetNumberOfItems)(void* self, uint32_t *numItems);
	HRESULT (*GetProperty)(void* self, uint32_t index, PROPID propID, PROPVARIANT *value);
	HRESULT (*Extract)(void* self, const uint32_t* indices, uint32_t numItems, uint32_t testMode, IArchiveExtractCallback *extractCallback);
	HRESULT (*GetArchiveProperty)(void* self, PROPID propID, PROPVARIANT *value);
	HRESULT (*GetNumberOfProperties)(void* self, uint32_t *numProperties);
	HRESULT (*GetPropertyInfo)(void* self, uint32_t index, wchar_t **name, PROPID *propID, VARTYPE *varType);
	HRESULT (*GetNumberOfArchiveProperties)(void* self, uint32_t *numProperties);
	HRESULT (*GetArchivePropertyInfo)(void* self, uint32_t index, wchar_t **name, PROPID *propID, VARTYPE *varType);
} _IInArchive_vtable;

typedef struct {
	_IInArchive_vtable* vtable;
} IInArchive;

typedef struct {
	$CDEF_IUnknown
	HRESULT(*GetNumberOfMethods)(void* self, uint32_t *numMethods);
	HRESULT(*GetProperty)(void* self, uint32_t index, PROPID propID, PROPVARIANT *value);
	HRESULT(*CreateDecoder)(void* self, uint32_t index, const GUID *iid, void **coder);
	HRESULT(*CreateEncoder)(void* self, uint32_t index, const GUID *iid, void **coder);
 } _ICompressCodecsInfo_vtable;

typedef struct {
	_ICompressCodecsInfo_vtable* vtable;
} ICompressCodecsInfo;

typedef struct {
	$CDEF_IUnknown
	HRESULT (*SetCompressCodecsInfo)(void* self, ICompressCodecsInfo *compressCodecsInfo);
} _ISetCompressCodecsInfo_vtable;

typedef struct {_ISetCompressCodecsInfo_vtable* vtable;} ISetCompressCodecsInfo;

typedef struct {
	$CDEF_IUnknown
	HRESULT (*CryptoGetTextPassword)(void* self, wchar_t **password);
} _ICryptoGetTextPassword_vtable;
typedef struct { _ICryptoGetTextPassword_vtable* vtable;} ICryptoGetTextPassword;

typedef struct {
	$CDEF_IUnknown
	HRESULT (*CryptoGetTextPassword2)(void* self, int* isdefined, wchar_t **password);
} _ICryptoGetTextPassword2_vtable;
typedef struct { _ICryptoGetTextPassword2_vtable* vtable;} ICryptoGetTextPassword2;

typedef struct {
	$CDEF_IUnknown
	HRESULT (*GetProperty)(void* self, PROPID propID, PROPVARIANT *value);
	HRESULT (*GetStream)(void* self, const wchar_t *name, IInStream **inStream);
} _IArchiveOpenVolumeCallback_vtable;
typedef struct { _IArchiveOpenVolumeCallback_vtable* vtable; } IArchiveOpenVolumeCallback;

typedef struct {
	$CDEF_IUnknown
	HRESULT (*SetSubArchiveName)(void* self, const wchar_t *name);
} _IArchiveOpenSetSubArchiveName_vtable;
typedef struct { _IArchiveOpenSetSubArchiveName_vtable* vtable; } IArchiveOpenSetSubArchiveName;
"""
).substitute(CDEF_IUnknown=CDEF_IUnknown)


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


def createIID(yy, xx):
    return uuid.UUID("{{23170F69-40C1-278A-0000-00{yy:s}00{xx:s}0000}}".format(xx=xx, yy=yy))


# 00 IProgress.h

IID_IProgress = createIID("00", "05")

# 01 IFolderArchive.h

IID_IArchiveFolder = createIID("01", "05")
IID_IFolderArchiveExtractCallback = createIID("01", "07")
IID_IOutFolderArchive = createIID("01", "0A")
IID_IFolderArchiveUpdateCallback = createIID("01", "0B")
IID_IArchiveFolderInternal = createIID("01", "0C")
IID_IInFolderArchive = createIID("01", "0E")

# 03 IStream.h

IID_ISequentialInStream = createIID("03", "01")
IID_ISequentialOutStream = createIID("03", "02")
IID_IInStream = createIID("03", "03")
IID_IOutStream = createIID("03", "04")
IID_IStreamGetSize = createIID("03", "06")
IID_IOutStreamFlush = createIID("03", "07")


# 04 ICoder.h

IID_ICompressProgressInfo = createIID("04", "04")
IID_ICompressCoder = createIID("04", "05")
IID_ICompressCoder2 = createIID("04", "18")
IID_ICompressSetCoderProperties = createIID("04", "20")
IID_ICompressSetDecoderProperties2 = createIID("04", "22")
IID_ICompressWriteCoderProperties = createIID("04", "23")
IID_ICompressGetInStreamProcessedSize = createIID("04", "24")
IID_ICompressSetCoderMt = createIID("04", "25")
IID_ICompressGetSubStreamSize = createIID("04", "30")
IID_ICompressSetInStream = createIID("04", "31")
IID_ICompressSetOutStream = createIID("04", "32")
IID_ICompressSetInStreamSize = createIID("04", "33")
IID_ICompressSetOutStreamSize = createIID("04", "34")
IID_ICompressSetBufSize = createIID("04", "35")
IID_ICompressFilter = createIID("04", "40")
IID_ICompressCodecsInfo = createIID("04", "60")
IID_ISetCompressCodecsInfo = createIID("04", "61")
IID_ICryptoProperties = createIID("04", "80")
IID_ICryptoResetSalt = createIID("04", "88")
IID_ICryptoResetInitVector = createIID("04", "8C")
IID_ICryptoSetPassword = createIID("04", "90")
IID_ICryptoSetCRC = createIID("04", "A0")


# 05 IPassword.h

IID_ICryptoGetTextPassword = createIID("05", "10")
IID_ICryptoGetTextPassword2 = createIID("05", "11")


# 06 IArchive.h

IID_ISetProperties = createIID("06", "03")
IID_IArchiveOpenCallback = createIID("06", "10")
IID_IArchiveExtractCallback = createIID("06", "20")
IID_IArchiveOpenVolumeCallback = createIID("06", "30")
IID_IInArchiveGetStream = createIID("06", "40")
IID_IArchiveOpenSetSubArchiveName = createIID("06", "50")
IID_IInArchive = createIID("06", "60")
IID_IArchiveOpenSeq = createIID("06", "61")

IID_IArchiveUpdateCallback = createIID("06", "80")
IID_IArchiveUpdateCallback2 = createIID("06", "82")
IID_IOutArchive = createIID("06", "A0")


# 08 IFolder.h
IID_IFolderFolder = createIID("08", "00")
IID_IEnumProperties = createIID("08", "01")
IID_IFolderGetTypeID = createIID("08", "02")
IID_IFolderGetPath = createIID("08", "03")
IID_IFolderWasChanged = createIID("08", "04")
IID_IFolderOperations = createIID("08", "06")
IID_IFolderGetSystemIconIndex = createIID("08", "07")
IID_IFolderGetItemFullSize = createIID("08", "08")
IID_IFolderClone = createIID("08", "09")
IID_IFolderSetFlatMode = createIID("08", "0A")
IID_IFolderOperationsExtractCallback = createIID("08", "0B")
IID_IFolderProperties = createIID("08", "0E")
IID_IFolderArcProps = createIID("08", "10")
IID_IGetFolderArcProps = createIID("08", "11")

# 09 IFolder.h :: FOLDER_MANAGER_INTERFACE
# IID_IFolderManager = createIID('09', '00')


# 0A PluginInterface.h
# IID_IInitContextMenu = createIID('0A', '0')
# IID_IPluginOptionsCallback = createIID('0A', '00')
# IID_IPluginOptions = createIID('0A', '0')

# PropID.h


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
    C_TIME = 10  # kpidCTime
    A_TIME = 11  # kpidATime
    M_TIME = 12  # kpidMTime
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
    SYM_LINK = 54  # kpidSymLink
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
    I_NODE = 91  # kpidINode
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


class OperationResult(Enum):
    kOK = 0
    kUnSupportedMethod = 1
    kDataError = 2
    kCRCError = 3


class AskMode(Enum):
    kExtract = 0
    kTest = 1
    kSkip = 2
