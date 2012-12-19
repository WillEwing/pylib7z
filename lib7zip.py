#!/usr/bin/env python2

from ctypes import *
import atexit

dll7z = cdll.LoadLibrary("libc7zip.dll")
range = xrange

lib = c_void_p()
lib = dll7z.create_C7ZipLibrary();
dll7z.c7zLib_Initialize(lib);

class NotSupportedArchive(Exception): pass

@atexit.register
def deinitialize():
	dll7z.c7zLib_Deinitialize(lib);
	dll7z.free_C7ZipLibrary(lib);
	
def get_supported_exts():
	num_exts = c_ulong();
	ext_array = pointer(c_wchar_p())
	dll7z.c7zLib_GetSupportedExts(lib, byref(ext_array), byref(num_exts))
	for i in range(num_exts.value):
		yield str(ext_array[i])
	dll7z.free_extarr(ext_array)

def openarchive(filename):
	instream = dll7z.create_c7zInSt_Filename(filename)
	ext = c_wchar_p(dll7z.c7zInSt_GetExt(instream))
	archive = c_void_p();
	dll7z.c7zLib_OpenArchive(lib, instream, byref(archive))
	if archive.value is None:
		raise IOError("Failed to open archive %s" % filename)
	elif dll7z.c7zLib_GetLastError(lib) == 4:
		raise NotSupportedArchive("Failed to open archive %s" % filename)
	elif dll7z.c7zLib_GetLastError(lib) != 0:
		raise Exception("Failed to open archive %s" % filename)
		
	return Archive(lib, archive, instream)

class Archive(object):
	def __init__(self, lib, archive, instream):
		self.lib = lib
		self.archive = archive
		self.instream = instream
	
	def __del__(self):
		dll7z.free_C7ZipInStream(self.instream)
		
	def __len__(self):
		item_count = c_ulong()
		dll7z.c7zArc_GetItemCount(self.archive, byref(item_count))
		return item_count.value
	
	def __getitem__(self,i):
		item = c_void_p()
		dll7z.c7zArc_GetItemInfo(self.archive, i, byref(item))
		return ArchiveItem(self.lib, self.archive, item)
	
	def __iter__(self):
		for i in range(len(self)):
			yield self[i]

class ArchiveItem(object):
	def __init__(self, lib, archive, item):
		self.lib = lib
		self.archive = archive
		self.item = item
	
	@property
	def path(self):
		return c_wchar_p(dll7z.c7zItm_GetFullPath(self.item)).value
	
	@property
	def isdir(self):
		return dll7z.c7zItm_IsDir(self.item)
	
	@property
	def crc(self):
		val = c_ulong()
		kpidCRC = 27-8;
		dll7z.c7zItm_GetUInt64Property(self.item, kpidCRC, byref(val))
		return val.value