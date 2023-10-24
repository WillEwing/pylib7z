#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python bindings for the 7-Zip Library: Archives
"""

from enum import KEEP, IntEnum, IntFlag
from io import BytesIO
from logging import getLogger
from os import SEEK_SET, PathLike
from pathlib import Path, PurePath
from types import TracebackType
from typing import Any, Dict, Generator, Optional, Self, Sequence, Type, Union
from weakref import ReferenceType, ref

from .extract_callback import (
    ArchiveExtractToDirectoryCallback,
    ArchiveExtractToStreamCallback,
    OperationResult,
)
from .ffi7zip import ffi, lib  # pylint: disable=no-name-in-module
from .format_registry import FormatInfo, formats
from .iids import (
    CreateObject,
    IID_IArchiveExtractCallback,
    IID_IArchiveOpenCallback,
    IID_IInArchive,
    IID_IInStream,
)
from .open_callback import ArchiveOpenCallback
from .propvariant import VARTYPE, PropVariant
from .stream import FileInStream

log = getLogger("lib7zip")


class ArchiveProps(IntEnum):
    """Archive and ArchiveItem Properties"""

    NO_PROPERTY_0 = 0
    MAIN_SUBFILE = 1
    HANDLER_ITEM_INDEX = 2
    PATH = 3
    NAME = 4
    EXTENSION = 5
    IS_DIR = 6
    SIZE = 7
    PACK_SIZE = 8
    ATTRIB = 9
    CTIME = 10
    ATIME = 11
    MTIME = 12
    SOLID = 13
    COMMENTED = 14
    ENCRYPTED = 15
    SPLIT_BEFORE = 16
    SPLIT_AFTER = 17
    DICTIONARY_SIZE = 18
    CRC = 19
    TYPE = 20
    IS_ANTI = 21
    METHOD = 22
    HOST_OS = 23
    FILE_SYSTEM = 24
    USER = 25
    GROUP = 26
    BLOCK = 27
    COMMENT = 28
    POSITION = 29
    PREFIX = 30
    NUM_SUB_DIRS = 31
    NUM_SUB_FILES = 32
    UNPACK_VER = 33
    VOLUME = 34
    IS_VOLUME = 35
    OFFSET = 36
    LINKS = 37
    NUM_BLOCKS = 38
    NUM_VOLUMES = 39
    TIME_TYPE = 40
    BIT64 = 41
    BIG_ENDIAN = 42
    CPU = 43
    PHY_SIZE = 44
    HEADERS_SIZE = 45
    CHECKSUM = 46
    CHARACTS = 47
    VA = 48
    ID = 49
    SHORT_NAME = 50
    CREATOR_APP = 51
    SECTOR_SIZE = 52
    POSIX_ATTRIB = 53
    SYM_LINK = 54
    ERROR = 55
    TOTAL_SIZE = 56
    FREE_SPACE = 57
    CLUSTER_SIZE = 58
    VOLUME_NAME = 59
    LOCAL_NAME = 60
    PROVIDER = 61
    NT_SECURE = 62
    IS_ALT_STREAM = 63
    IS_AUX = 64
    IS_DELETED = 65
    IS_TREE = 66
    SHA1 = 67
    SHA256 = 68
    ERROR_TYPE = 69
    NUM_ERRORS = 70
    ERROR_FLAGS = 71
    WARNING_FLAGS = 72
    WARNING = 73
    NUM_STREAMS = 74
    NUM_ALT_STREAMS = 75
    ALT_STREAMS_SIZE = 76
    VIRTUAL_SIZE = 77
    UNPACK_SIZE = 78
    TOTAL_PHY_SIZE = 79
    VOLUME_INDEX = 80
    SUB_TYPE = 81
    SHORT_COMMENT = 82
    CODE_PAGE = 83
    IS_NOT_ARC_TYPE = 84
    PHY_SIZE_CANT_BE_DETECTED = 85
    ZEROS_TAIL_IS_ALLOWED = 86
    TAIL_SIZE = 87
    EMBEDDED_STUB_SIZE = 88
    NT_REPARSE = 89
    HARD_LINK = 90
    INODE = 91
    STREAM_ID = 92
    READ_ONLY = 93
    OUT_NAME = 94
    COPY_LINK = 95
    ARC_FILE_NAME = 96
    IS_HASH = 97
    CHANGE_TIME = 98
    USER_ID = 99
    GROUP_ID = 100
    DEVICE_MAJOR = 101
    DEVICE_MINOR = 102
    DEV_MAJOR = 103
    DEV_MINOR = 104


class ArchiveItemAttrib(IntFlag, boundary=KEEP):
    """
    Archive item attribute flags.
    """

    READ_ONLY = 1 << 0
    HIDDEN = 1 << 1
    SYSTEM = 1 << 2
    DIRECTORY = 1 << 3
    ARCHIVE = 1 << 4
    DEVICE = 1 << 5
    NORMAL = 1 << 6
    TEMPORARY = 1 << 7
    SPARSE_FILE = 1 << 8
    REPARSE_POINT = 1 << 9
    COMPRESSED = 1 << 10
    OFFLINE = 1 << 11
    ENCRYPTED = 1 << 12
    UNIX_EXTENSION = 1 << 13


class ArchiveError(RuntimeError):
    pass


class ArchiveClosedError(ArchiveError):
    pass


class ExtractError(ArchiveError):
    pass


class NotAFileError(ExtractError):
    pass


class NotThisArchiveError(ArchiveError):
    pass


class Archive:
    """An archive."""

    closed: bool
    _archive_properties: Dict[str, int]
    _archive_item_properties: Dict[str, int]
    _item_indices_by_path: Dict[PurePath, int]

    def __init__(self, filename: Union[PathLike, str], *, password: Union[None, str, bytes] = None) -> None:
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

        try:
            self.__read_archive_properties()
            self.__read_archive_item_properties()
        except Exception:
            log.exception("Failed reading archive (item) property information.")
            self.close()
            raise

        self.__items_by_path = {}

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
        result = archive.vtable.Open(archive, stream, ffi.NULL, open_callback)  # type: ignore
        if result & 0x80000000:
            ffi.release(archive)
            return False

        self.archive = archive
        return True

    def __read_properties(self, get_num_props_fn, get_prop_fn) -> Dict[str, int]:
        arc = self.archive
        with ffi.new("uint32_t *") as num_props_ptr:
            result = get_num_props_fn(arc, num_props_ptr)
            if result & 0x80000000:
                raise RuntimeError(f"HRESULT(0x{result:#08x})")
            num_props = num_props_ptr[0]

        properties: Dict[str, int] = {}

        name_ptr = ffi.new("wchar_t **")
        prop_id_ptr = ffi.new("PROPID *")
        var_type_ptr = ffi.new("VARTYPE *")

        for prop_idx in range(num_props):
            result = get_prop_fn(arc, prop_idx, name_ptr, prop_id_ptr, var_type_ptr)
            if result & 0x80000000:
                raise RuntimeError(f"HRESULT(0x{result:#08x})")

            prop_id = prop_id_ptr[0]
            prop_name: str = ""
            if name_ptr[0] != ffi.NULL:
                name_str = ffi.string(name_ptr[0])
                assert isinstance(name_str, str)
                prop_name = name_str
                lib.SysFreeString(name_ptr[0])  # type: ignore

            if prop_id < 0x10000:
                try:
                    prop_id = ArchiveProps(prop_id)
                    prop_name = prop_id.name.lower()
                except ValueError:
                    log.warning("Unknown 7-zip archive property: %d", prop_id)
                    continue

            prop_name = prop_name.lower()
            prop_type = VARTYPE(var_type_ptr[0])

            log.debug("Got property %d: %s (type: %s)", prop_id, prop_name, prop_type.name)
            properties[prop_name] = prop_id

        ffi.release(var_type_ptr)
        ffi.release(prop_id_ptr)
        ffi.release(name_ptr)

        return properties

    def __read_archive_properties(self) -> None:
        log.debug("Reading archive property info.")
        self._archive_properties = self.__read_properties(
            self.archive.vtable.GetNumberOfArchiveProperties,
            self.archive.vtable.GetArchivePropertyInfo,
        )

    def __read_archive_item_properties(self) -> None:
        log.debug("Reading archive item property info.")
        self._archive_item_properties = self.__read_properties(
            self.archive.vtable.GetNumberOfProperties,
            self.archive.vtable.GetPropertyInfo,
        )

    def __len__(self) -> int:
        if self.closed:
            raise ArchiveClosedError()
        number_of_items = ffi.new("uint32_t *")
        result = self.archive.vtable.GetNumberOfItems(self.archive, number_of_items)  # type: ignore
        if result & 0x80000000:
            raise RuntimeError()
        return number_of_items[0]

    def __getitem__(self, index: int | PathLike | str):
        if self.closed:
            raise ArchiveClosedError()
        if not isinstance(index, int):
            index = PurePath(index)
            if not self._item_indices_by_path:
                self._item_indices_by_path = {PurePath(item.path): item.index for item in self}
            try:
                return ArchiveItem(self, self._item_indices_by_path[index])
            except KeyError as exc:
                raise FileNotFoundError() from exc
        if not (0 <= index < len(self)):
            raise IndexError()
        return ArchiveItem(self, index)

    def __iter__(self):
        num_items = len(self)
        for index in range(num_items):
            yield self[index]

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
                raise NotThisArchiveError()
            item_indices.add(item.index)
        return sorted(item_indices)

    def extract(self, dest_dir: PathLike, items: Optional[Sequence["ArchiveItem"]] = None, **kwargs) -> None:
        """Extract files into a directory."""
        if self.closed:
            raise ArchiveClosedError()

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
        extract_callback = ArchiveExtractToDirectoryCallback(archive=self, directory=dest_dir, password=self.password, **kwargs)
        extract_callback_instance = extract_callback.get_instance(IID_IArchiveExtractCallback)
        result = archive.vtable.Extract(archive, items_ptr, num_items, 0, extract_callback_instance)  # type: ignore
        extract_callback.cleanup()
        if result & 0x80000000:
            raise ExtractError(f"HRESULT(0x{result:#08x})")
        if extract_callback.last_op_result != OperationResult.OK:
            raise ExtractError()

    def read_item_bytes(self, item: "ArchiveItem", *, password: Union[None, str, bytes] = None) -> bytes:
        """Read `item` as bytes."""
        if self.closed:
            raise ArchiveClosedError()
        if item.archive() != self:
            raise ValueError()

        item_ptr = ffi.new("uint32_t*", item.index)

        item_stream = BytesIO()
        archive = self.archive
        extract_callback = ArchiveExtractToStreamCallback(item_stream, item.index, password)
        extract_callback_instance = extract_callback.get_instance(IID_IArchiveExtractCallback)
        result = archive.vtable.Extract(archive, item_ptr, 1, 0, extract_callback_instance)  # type: ignore
        extract_callback.cleanup()
        if result & 0x80000000:
            raise ExtractError(f"HRESULT(0x{result:#08x})")
        if extract_callback.last_op_result != OperationResult.OK:
            raise ExtractError()

        return item_stream.getvalue()

    def read_item_text(self, item: "ArchiveItem", encoding: str = "utf-8", *, password: Union[None, str, bytes] = None) -> str:
        """Read `item` as text."""
        return str(self.read_item_bytes(item, password=password), encoding=encoding)


class ArchiveItem:
    """An item inside an Archive."""

    _properties: Dict[str, int]
    archive: ReferenceType[Archive]
    index: int

    def __init__(self, archive: Archive, index: int) -> None:
        if not (0 <= index < len(archive)):
            raise IndexError
        self._properties = archive._archive_item_properties
        self.archive = ref(archive)
        self.index = index

    def read_bytes(self, *, password: Union[None, str, bytes] = None) -> bytes:
        """Read the contents of the item as a bytes."""
        archive = self.archive()
        if not archive or archive.closed:
            raise ArchiveClosedError()
        return archive.read_item_bytes(self, password=password)

    def read_text(self, encoding: str = "utf-8", *, password: Union[None, str, bytes] = None) -> str:
        """Read the contents of the item as a string."""
        archive = self.archive()
        if not archive or archive.closed:
            raise ArchiveClosedError()
        return archive.read_item_text(self, encoding, password=password)

    def __get_prop_impl(self, prop_id: int) -> Any:
        archive = self.archive()
        if not archive or archive.closed:
            raise ArchiveClosedError()
        arc = archive.archive
        prop_var = PropVariant()
        result = arc.vtable.GetProperty(arc, self.index, prop_id, prop_var.cdata)
        if result & 0x80000000:
            raise ArchiveError(f"HRESULT(0x{result:#08x})")
        return prop_var.as_any()

    def __getattr__(self, name: str) -> Any:
        try:
            if not name.islower():
                raise ValueError()
            prop_id = ArchiveProps[name.upper()]
            return self.__get_prop_impl(prop_id)
        except ValueError as exc:
            raise AttributeError from exc
