# -*- coding: utf-8 -*-
import io
import os.path
from functools import partial
from weakref import ref

from . import Format, dll7z, ffi, formats, log, max_sig_size, py7ziptypes
from .cmpcodecsinfo import CompressCodecsInfo
from .extract_callback import (
    ArchiveExtractToDirectoryCallback,
    ArchiveExtractToStreamCallback,
)
from .open_callback import ArchiveOpenCallback
from .stream import FileInStream
from .winhelpers import RNOK, get_prop_val, uuid2guidp


class Archive:
    def __init__(self, filename, forcetype=None, password=None):
        self.filename = filename
        self.password = password
        self._path2idx = {}
        self._idx2itm = {}
        self._num_items = None

        self.stream = FileInStream(filename)
        stream_inst = self.stream.instances[py7ziptypes.IID_IInStream]

        if forcetype is not None:
            possible_formats = [formats[forcetype]]
        else:
            possible_formats = self._get_possible_formats()

        for format in possible_formats:
            if self._try_open_format(format):
                break
        else:
            raise RuntimeError("%r: No format", self.filename)

        archive = self.archive

        log.debug("creating callback obj")
        self.open_cb = callback = ArchiveOpenCallback(password=password)
        self.open_cb_i = callback_inst = callback.instances[py7ziptypes.IID_IArchiveOpenCallback]

        set_cmpcodecsinfo_ptr = ffi.new("void**")
        archive.vtable.QueryInterface(archive, uuid2guidp(py7ziptypes.IID_ISetCompressCodecsInfo), set_cmpcodecsinfo_ptr)

        if set_cmpcodecsinfo_ptr != ffi.NULL:
            log.debug("Setting Compression Codec Info")
            self.set_cmpcodecs_info = set_cmpcodecsinfo = ffi.cast("ISetCompressCodecsInfo*", set_cmpcodecsinfo_ptr[0])

            # TODO...
            cmp_codec_info = CompressCodecsInfo()
            cmp_codec_info_inst = cmp_codec_info.instances[py7ziptypes.IID_ICompressCodecsInfo]
            set_cmpcodecsinfo.vtable.SetCompressCodecsInfo(set_cmpcodecsinfo, cmp_codec_info_inst)
            log.debug("compression codec info set")

        # old_vtable = archive.vtable
        log.debug("opening archive")
        maxCheckStartPosition = ffi.NULL  # ffi.new("uint64_t*", 1 << 22)
        RNOK(archive.vtable.Open(archive, stream_inst, maxCheckStartPosition, callback_inst))
        self.itm_prop_fn = partial(archive.vtable.GetProperty, archive)
        # log.debug('what now?')

        # import pdb; pdb.set_trace()
        # archive.vtable = old_vtable
        # tmp_archive2 = ffi.new('void**')
        # RNOK(self.archive.vtable.QueryInterface(archive, iid, tmp_archive2))
        # self.archive = archive = ffi.cast('IInArchive*', tmp_archive2[0])
        # self.tmp_archive = tmp_archive2

        assert archive.vtable.GetNumberOfItems != ffi.NULL
        assert archive.vtable.GetProperty != ffi.NULL
        log.debug("successfully opened archive")

    def _try_open_format(self, format: Format) -> bool:
        log.debug("Trying to open archive %r as format %s.", self.filename, format.name)

        iid = uuid2guidp(py7ziptypes.IID_IInArchive)
        classid = uuid2guidp(format.classid)

        archive_raw = ffi.new("void**")
        RNOK(dll7z.CreateObject(classid, iid, archive_raw))

        if archive_raw[0] == ffi.NULL:
            return False

        self.archive_raw = archive_raw
        self.archive = ffi.cast("IInArchive*", archive_raw[0])

        assert self.archive.vtable.GetNumberOfItems != ffi.NULL
        assert self.archive.vtable.GetProperty != ffi.NULL

        return True

    def _get_possible_formats(self) -> list[Format]:
        file = self.stream.filelike
        sig_buf = file.read(max_sig_size)
        file.seek(0)

        possible_formats = []
        for format in formats.values():
            if format.signatures and format.signature_offset == 0 and not any((sig_buf[: len(sig)] for sig in format.signatures)):
                continue
            # TODO: Handle 'backward open' files.
            if not any(self.filename.endswith(f".{ext}") for ext in format.extensions):
                continue
            possible_formats.append(format)

        return possible_formats

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        log.debug("Archive.close()")
        if self.archive == ffi.NULL or self.archive.vtable == ffi.NULL or self.archive.vtable.Close == ffi.NULL:
            log.warn("close failed, NULLs")
            return
        RNOK(self.archive.vtable.Close(self.archive))

    def __len__(self):
        log.debug("len(Archive)")
        if self._num_items is None:
            num_items = ffi.new("uint32_t*")
            # import pdb; pdb.set_trace()
            assert self.archive.vtable.GetNumberOfItems != ffi.NULL
            RNOK(self.archive.vtable.GetNumberOfItems(self.archive, num_items))
            log.debug("num_items=%d", int(num_items[0]))
            self._num_items = int(num_items[0])

        return self._num_items

    def get_by_index(self, index):
        log.debug("Archive.get_by_index(%d)", index)
        try:
            return self._idx2itm[index]
        except KeyError:
            itm = ArchiveItem(self, index)
            self._idx2itm[index] = itm
            return itm

    def __getitem__(self, index):
        log.debug("Archive[%r]", index)
        if isinstance(index, int):
            if index > len(self):
                raise IndexError(index)
            return self.get_by_index(index)
        else:
            if index not in self._path2index:
                found_path = False
                for item in self:
                    if item.path == index:
                        self._path2index[index] = item.index
                        found_path = True
                if not found_path:
                    raise KeyError(index)
            return self.get_by_index(self._path2index[index])

    def __iter__(self):
        log.debug("iter(Archive)")
        for i in range(len(self)):
            log.debug("getting %dth item", i)
            yield self[i]
            # isdir = get_bool_prop(i, py7ziptypes.kpidIsDir, self.itm_prop_fn)
            # path = get_string_prop(i, py7ziptypes.kpidPath, self.itm_prop_fn)
            # crc = get_hex_prop(i, py7ziptypes.kpidCRC, self.itm_prop_fn)
            # yield isdir, path, crc

    def __getattr__(self, attr):
        pass

    def extract(self, directory="", password=None):
        log.debug("Archive.extract()")
        """
			IInArchive::Extract:
			indices must be sorted
			numItems = 0xFFFFFFFF means "all files"
			testMode != 0 means "test files without writing to outStream"
		"""

        password = password or self.password

        callback = ArchiveExtractToDirectoryCallback(self, directory, password)
        callback_inst = callback.instances[py7ziptypes.IID_IArchiveExtractCallback]
        assert self.archive.vtable.Extract != ffi.NULL
        # import pdb; pdb.set_trace()
        log.debug("started extract")
        RNOK(self.archive.vtable.Extract(self.archive, ffi.NULL, 0xFFFFFFFF, 0, callback_inst))
        log.debug("finished extract")
        log.debug("totally done")


class ArchiveItem:
    def __init__(self, archive, index):
        self.archive_ref = ref(archive)
        self.index = index
        self._contents = None
        self.password = None

    def extract(self, file, password=None):
        archive = self.archive_ref()
        password = password or self.password or archive.password

        self.callback = callback = ArchiveExtractToStreamCallback(file, self.index, password)
        self.cb_inst = callback_inst = callback.instances[py7ziptypes.IID_IArchiveExtractCallback]
        RNOK(archive.archive.vtable.Extract(archive.archive, ffi.NULL, 0xFFFFFFFF, 0, callback_inst))

    @property
    def contents(self):
        # import pdb; pdb.set_trace()
        if self._contents is None:
            stream = io.BytesIO()
            self.extract(stream)
            self._contents = stream.getvalue()

        return self._contents

    def __getattr__(self, attr: str):
        archive = self.archive_ref()
        if not attr.islower():
            raise AttributeError()
        propid = getattr(py7ziptypes.ArchiveProps, attr.upper())
        return get_prop_val(partial(archive.itm_prop_fn, self.index, propid))
