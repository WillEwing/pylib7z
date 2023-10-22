#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python bindings for the 7-Zip Library: Archives
"""

from enum import IntEnum
from io import BytesIO
from os import SEEK_SET, PathLike
from pathlib import Path
from types import TracebackType
from typing import Generator, Optional, Self, Sequence, Type, Union
from weakref import ReferenceType, ref

from .extract_callback import (
    ArchiveExtractToDirectoryCallback,
    ArchiveExtractToStreamCallback,
)
from .ffi7zip import ffi  # pylint: disable=no-name-in-module
from .format_registry import FormatInfo, formats
from .iids import (
    CreateObject,
    IID_IArchiveExtractCallback,
    IID_IArchiveOpenCallback,
    IID_IInArchive,
    IID_IInStream,
)
from .open_callback import ArchiveOpenCallback
from .propvariant import PropVariant
from .stream import FileInStream


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


class Archive:
    """An archive."""

    closed: bool

    def __init__(self, filename: PathLike, *, password: Union[None, str, bytes] = None) -> None:
        self.filename = filename
        self.password = password

        self.stream = FileInStream(filename)
        self.open_callback = ArchiveOpenCallback(password=password, stream=self.stream)

        for fmt in self.__get_possible_formats():
            if self.__try_open_as_format(fmt):
                break
        else:
            raise RuntimeError("{self.filename}: Unknown or unsupported format.")

        self.closed = False

    def __get_possible_formats(self) -> Generator[FormatInfo, None, None]:
        extension = None
        if suffix := Path(self.filename).suffix:
            extension = suffix[1:]
        for fmt in formats:
            if extension and extension not in fmt.extensions:
                continue
            yield fmt

    def __try_open_as_format(self, fmt: FormatInfo) -> bool:
        try:
            archive = CreateObject(fmt.clsid, IID_IInArchive)
        except RuntimeError:
            return False
        self.stream.stream.seek(0, SEEK_SET)
        stream = self.stream.get_instance(IID_IInStream)
        open_callback = self.open_callback.get_instance(IID_IArchiveOpenCallback)
        result = archive.vtable.Open(archive, stream, ffi.NULL, open_callback)
        if result < 0:
            archive.release()
            return False

        self.archive = archive
        return True

    def __len__(self) -> int:
        number_of_items = ffi.new("uint32_t *")
        result = self.archive.vtable.GetNumberOfItems(self.archive, number_of_items)
        if result < 0:
            raise RuntimeError()
        return number_of_items[0]

    def __getitem__(self, index):
        if not (0 <= index < len(self)):
            raise IndexError()
        return ArchiveItem(self, index)

    def close(self):
        """Explicitly close the Archive and free its resources."""
        if not self.closed:
            self.archive.vtable.Close(self.archive)
            ffi.release(self.archive)
        self.closed = True

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.close()

    def __to_item_indices(self, items: Sequence["ArchiveItem"]) -> list[int]:
        item_indices: set[int] = set()
        for item in items:
            if item.archive() != self:
                raise ValueError()
            item_indices.add(item.index)
        return sorted(item_indices)

    def extract(self, dest_dir: PathLike, items: Optional[Sequence["ArchiveItem"]] = None) -> None:
        """Extract files into a directory."""
        if not items and items is not None:
            # The caller has specified which files to extract, and it's none of them.
            return

        items_ptr: ffi.CData = ffi.NULL  # type: ignore
        num_items = 0xFFFFFFFF
        if items:
            indices = self.__to_item_indices(items)
            items_ptr = ffi.new("uint32_t []", indices)
            num_items = len(indices)

        archive = self.archive
        extract_callback = ArchiveExtractToDirectoryCallback(archive=self, directory=dest_dir, password=None)
        extract_callback_instance = extract_callback.get_instance(IID_IArchiveExtractCallback)
        result = archive.vtable.Extract(archive, items_ptr, num_items, 0, extract_callback_instance)
        extract_callback.cleanup()
        if result < 0:
            raise RuntimeError(f"HRESULT(0x{result:#08x})")

    def read_item_bytes(self, item: "ArchiveItem", *, password: Union[None, str, bytes] = None) -> bytes:
        if item.archive() != self:
            raise ValueError()

        item_ptr = ffi.new("uint32_t*", item.index)

        item_stream = BytesIO()
        archive = self.archive
        extract_callback = ArchiveExtractToStreamCallback(item_stream, item.index, password)
        extract_callback_instance = extract_callback.get_instance(IID_IArchiveExtractCallback)
        result = archive.vtable.Extract(archive, item_ptr, 1, 0, extract_callback_instance)
        if result < 0:
            raise RuntimeError(f"HRESULT(0x{result:#08x})")
        extract_callback.cleanup()
        return item_stream.getvalue()

    def read_item_text(self, item: "ArchiveItem", encoding: str = "utf-8", *, password: Union[None, str, bytes] = None) -> str:
        return str(self.read_item_bytes(item, password=password), encoding=encoding)


class ArchiveItem:
    """An item inside an Archive."""

    archive: ReferenceType[Archive]
    index: int

    def __init__(self, archive: Archive, index: int) -> None:
        if not (0 <= index < len(archive)):
            raise IndexError
        self.archive = ref(archive)
        self.index = index

    def __get_property(self, prop_id) -> PropVariant:
        archive = self.archive()
        if not archive or archive.closed:
            raise RuntimeError()

        prop_var = PropVariant()
        result = archive.archive.vtable.GetProperty(archive.archive, self.index, prop_id, prop_var.cdata)
        if result < 0:
            raise RuntimeError()
        return prop_var

    def read_bytes(self, *, password: Union[None, str, bytes] = None) -> bytes:
        archive = self.archive()
        if not archive or archive.closed:
            raise RuntimeError()
        return archive.read_item_bytes(self, password=password)

    def read_text(self, encoding: str = "utf-8", *, password: Union[None, str, bytes] = None) -> str:
        archive = self.archive()
        if not archive or archive.closed:
            raise RuntimeError()
        return archive.read_item_text(self, encoding, password=password)

    @property
    def path(self) -> str:
        """The path of the item."""
        return self.__get_property(ArchiveProps.PATH).as_string()

    @property
    def is_dir(self) -> bool:
        """is the item a directory."""
        return self.__get_property(ArchiveProps.IS_DIR).as_bool()

    @property
    def crc(self) -> Optional[int]:
        """Item CRC"""
        prop_var = self.__get_property(ArchiveProps.CRC)
        if not prop_var.has_value:
            return None
        return prop_var.as_int()
