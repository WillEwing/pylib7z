/* - BEGIN GENERATED CIMPL - */
typedef struct FFI7Z_IUnknown_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
} FFI7Z_IUnknown_vtable;

typedef struct FFI7Z_IUnknown_tag {
    FFI7Z_IUnknown_vtable * vtable;
} FFI7Z_IUnknown;

typedef struct FFI7Z_PyIUnknown_tag {
    FFI7Z_IUnknown_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyIUnknown;

typedef struct FFI7Z_ISequentialInStream_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
    HRESULT (WINAPI *Read)(void* self, void * data, uint32_t size, uint32_t * processed_size);
} FFI7Z_ISequentialInStream_vtable;

typedef struct FFI7Z_ISequentialInStream_tag {
    FFI7Z_ISequentialInStream_vtable * vtable;
} FFI7Z_ISequentialInStream;

typedef struct FFI7Z_PyISequentialInStream_tag {
    FFI7Z_ISequentialInStream_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyISequentialInStream;

typedef struct FFI7Z_IInStream_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
    HRESULT (WINAPI *Read)(void* self, void * data, uint32_t size, uint32_t * processed_size);
    HRESULT (WINAPI *Seek)(void* self, int64_t offset, uint32_t seekOrigin, uint64_t * newPosition);
} FFI7Z_IInStream_vtable;

typedef struct FFI7Z_IInStream_tag {
    FFI7Z_IInStream_vtable * vtable;
} FFI7Z_IInStream;

typedef struct FFI7Z_PyIInStream_tag {
    FFI7Z_IInStream_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyIInStream;

typedef struct FFI7Z_ISequentialOutStream_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
    HRESULT (WINAPI *Write)(void* self, const void * data, uint32_t size, uint32_t * processed_size);
} FFI7Z_ISequentialOutStream_vtable;

typedef struct FFI7Z_ISequentialOutStream_tag {
    FFI7Z_ISequentialOutStream_vtable * vtable;
} FFI7Z_ISequentialOutStream;

typedef struct FFI7Z_PyISequentialOutStream_tag {
    FFI7Z_ISequentialOutStream_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyISequentialOutStream;

typedef struct FFI7Z_IOutStream_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
    HRESULT (WINAPI *Write)(void* self, const void * data, uint32_t size, uint32_t * processed_size);
    HRESULT (WINAPI *Seek)(void* self, int64_t offset, uint32_t seekOrigin, uint64_t * newPosition);
} FFI7Z_IOutStream_vtable;

typedef struct FFI7Z_IOutStream_tag {
    FFI7Z_IOutStream_vtable * vtable;
} FFI7Z_IOutStream;

typedef struct FFI7Z_PyIOutStream_tag {
    FFI7Z_IOutStream_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyIOutStream;

typedef struct FFI7Z_IProgress_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
    HRESULT (WINAPI *SetTotal)(void* self, uint64_t total);
    HRESULT (WINAPI *SetCompleted)(void* self, const uint64_t * complete_value);
} FFI7Z_IProgress_vtable;

typedef struct FFI7Z_IProgress_tag {
    FFI7Z_IProgress_vtable * vtable;
} FFI7Z_IProgress;

typedef struct FFI7Z_PyIProgress_tag {
    FFI7Z_IProgress_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyIProgress;

typedef struct FFI7Z_IArchiveExtractCallback_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
    HRESULT (WINAPI *SetTotal)(void* self, uint64_t total);
    HRESULT (WINAPI *SetCompleted)(void* self, const uint64_t * complete_value);
    HRESULT (WINAPI *GetStream)(void* self, uint32_t index, FFI7Z_ISequentialOutStream * out_stream, int32_t ask_extract_mode);
    HRESULT (WINAPI *PrepareOperation)(void* self, int32_t ask_extract_mode);
    HRESULT (WINAPI *SetOperationResult)(void* self, int32_t op_result);
} FFI7Z_IArchiveExtractCallback_vtable;

typedef struct FFI7Z_IArchiveExtractCallback_tag {
    FFI7Z_IArchiveExtractCallback_vtable * vtable;
} FFI7Z_IArchiveExtractCallback;

typedef struct FFI7Z_PyIArchiveExtractCallback_tag {
    FFI7Z_IArchiveExtractCallback_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyIArchiveExtractCallback;

typedef struct FFI7Z_IArchiveOpenCallback_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
    HRESULT (WINAPI *SetTotal)(void* self, const uint64_t * files, const uint64_t * bytes);
    HRESULT (WINAPI *SetCompleted)(void* self, const uint64_t * files, const uint64_t * bytes);
} FFI7Z_IArchiveOpenCallback_vtable;

typedef struct FFI7Z_IArchiveOpenCallback_tag {
    FFI7Z_IArchiveOpenCallback_vtable * vtable;
} FFI7Z_IArchiveOpenCallback;

typedef struct FFI7Z_PyIArchiveOpenCallback_tag {
    FFI7Z_IArchiveOpenCallback_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyIArchiveOpenCallback;

typedef struct FFI7Z_IArchiveOpenSetSubArchiveName_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
    HRESULT (WINAPI *SetSubArchiveName)(void* self, const wchar_t * name);
} FFI7Z_IArchiveOpenSetSubArchiveName_vtable;

typedef struct FFI7Z_IArchiveOpenSetSubArchiveName_tag {
    FFI7Z_IArchiveOpenSetSubArchiveName_vtable * vtable;
} FFI7Z_IArchiveOpenSetSubArchiveName;

typedef struct FFI7Z_PyIArchiveOpenSetSubArchiveName_tag {
    FFI7Z_IArchiveOpenSetSubArchiveName_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyIArchiveOpenSetSubArchiveName;

typedef struct FFI7Z_IArchiveOpenVolumeCallback_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
    HRESULT (WINAPI *GetProperty)(void* self, PROPID prop_id, PROPVARIANT * value);
    HRESULT (WINAPI *GetStream)(void* self, const wchar_t * name, FFI7Z_IInStream ** in_stream);
} FFI7Z_IArchiveOpenVolumeCallback_vtable;

typedef struct FFI7Z_IArchiveOpenVolumeCallback_tag {
    FFI7Z_IArchiveOpenVolumeCallback_vtable * vtable;
} FFI7Z_IArchiveOpenVolumeCallback;

typedef struct FFI7Z_PyIArchiveOpenVolumeCallback_tag {
    FFI7Z_IArchiveOpenVolumeCallback_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyIArchiveOpenVolumeCallback;

typedef struct FFI7Z_ICompressCodecsInfo_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
    HRESULT (WINAPI *GetNumMethods)(void* self, uint32_t * num_methods);
    HRESULT (WINAPI *GetProperty)(void* self, uint32_t index, PROPID prop_id, PROPVARIANT * value);
    HRESULT (WINAPI *CreateDecoder)(void* self, uint32_t index, const GUID * iid, void ** coder);
    HRESULT (WINAPI *CreateEncoder)(void* self, uint32_t index, const GUID * iid, void ** coder);
} FFI7Z_ICompressCodecsInfo_vtable;

typedef struct FFI7Z_ICompressCodecsInfo_tag {
    FFI7Z_ICompressCodecsInfo_vtable * vtable;
} FFI7Z_ICompressCodecsInfo;

typedef struct FFI7Z_PyICompressCodecsInfo_tag {
    FFI7Z_ICompressCodecsInfo_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyICompressCodecsInfo;

typedef struct FFI7Z_ICompressProgressInfo_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
    HRESULT (WINAPI *SetRatioInfo)(void* self, const uint64_t * in_size, const uint64_t * out_size);
} FFI7Z_ICompressProgressInfo_vtable;

typedef struct FFI7Z_ICompressProgressInfo_tag {
    FFI7Z_ICompressProgressInfo_vtable * vtable;
} FFI7Z_ICompressProgressInfo;

typedef struct FFI7Z_PyICompressProgressInfo_tag {
    FFI7Z_ICompressProgressInfo_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyICompressProgressInfo;

typedef struct FFI7Z_ICryptoGetTextPassword_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
    HRESULT (WINAPI *CryptoGetTextPassword)(void* self, wchar_t ** password);
} FFI7Z_ICryptoGetTextPassword_vtable;

typedef struct FFI7Z_ICryptoGetTextPassword_tag {
    FFI7Z_ICryptoGetTextPassword_vtable * vtable;
} FFI7Z_ICryptoGetTextPassword;

typedef struct FFI7Z_PyICryptoGetTextPassword_tag {
    FFI7Z_ICryptoGetTextPassword_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyICryptoGetTextPassword;

typedef struct FFI7Z_ICryptoGetTextPassword2_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
    HRESULT (WINAPI *CryptoGetTextPassword2)(void* self, int32_t * password_is_defined, wchar_t ** password);
} FFI7Z_ICryptoGetTextPassword2_vtable;

typedef struct FFI7Z_ICryptoGetTextPassword2_tag {
    FFI7Z_ICryptoGetTextPassword2_vtable * vtable;
} FFI7Z_ICryptoGetTextPassword2;

typedef struct FFI7Z_PyICryptoGetTextPassword2_tag {
    FFI7Z_ICryptoGetTextPassword2_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyICryptoGetTextPassword2;

typedef struct FFI7Z_IInArchive_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
    HRESULT (WINAPI *Open)(void* self, FFI7Z_IInStream * stream, const uint64_t * max_check_start_position, FFI7Z_IArchiveOpenCallback * open_callback);
    HRESULT (WINAPI *Close)(void* self);
    HRESULT (WINAPI *GetNumberOfItems)(void* self, uint32_t * num_items);
    HRESULT (WINAPI *GetProperty)(void* self, uint32_t index, PROPID prop_id, PROPVARIANT * value);
    HRESULT (WINAPI *Extract)(void* self, const uint32_t * indices, uint32_t num_items, int32_t test_mode, FFI7Z_IArchiveExtractCallback * extract_callback);
    HRESULT (WINAPI *GetArchiveProperty)(void* self, PROPID prop_id, PROPVARIANT * value);
    HRESULT (WINAPI *GetNumberOfProperties)(void* self, uint32_t * num_props);
    HRESULT (WINAPI *GetPropertyInfo)(void* self, uint32_t index, wchar_t ** name, PROPID * prop_id, VARTYPE * var_type);
    HRESULT (WINAPI *GetNumberOfArchiveProperties)(void* self, uint32_t * num_properties);
    HRESULT (WINAPI *GetArchivePropertyInfo)(void* self, uint32_t index, wchar_t ** name, PROPID * prop_id, VARTYPE * var_type);
} FFI7Z_IInArchive_vtable;

typedef struct FFI7Z_IInArchive_tag {
    FFI7Z_IInArchive_vtable * vtable;
} FFI7Z_IInArchive;

typedef struct FFI7Z_PyIInArchive_tag {
    FFI7Z_IInArchive_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyIInArchive;

typedef struct FFI7Z_ISetCompressCodecsInfo_vtable_tag {
    HRESULT (WINAPI *QueryInterface)(void* self, GUID * iid, void ** out_object);
    uint32_t (WINAPI *AddRef)(void* self);
    uint32_t (WINAPI *Release)(void* self);
    HRESULT (WINAPI *SetCompressCodecsInfo)(void* self, FFI7Z_ICompressCodecsInfo * compress_codecs_info);
} FFI7Z_ISetCompressCodecsInfo_vtable;

typedef struct FFI7Z_ISetCompressCodecsInfo_tag {
    FFI7Z_ISetCompressCodecsInfo_vtable * vtable;
} FFI7Z_ISetCompressCodecsInfo;

typedef struct FFI7Z_PyISetCompressCodecsInfo_tag {
    FFI7Z_ISetCompressCodecsInfo_vtable * vtable;
    void * pyojbect_tag;
} FFI7Z_PyISetCompressCodecsInfo;


HRESULT WINAPI FFI7Z_Py_IUnknown_QueryInterface(void* self, GUID * iid, void ** out_object);
uint32_t WINAPI FFI7Z_Py_IUnknown_AddRef(void* self);
uint32_t WINAPI FFI7Z_Py_IUnknown_Release(void* self);
HRESULT WINAPI FFI7Z_Py_ISequentialInStream_Read(void* self, void * data, uint32_t size, uint32_t * processed_size);
HRESULT WINAPI FFI7Z_Py_IInStream_Seek(void* self, int64_t offset, uint32_t seekOrigin, uint64_t * newPosition);
HRESULT WINAPI FFI7Z_Py_ISequentialOutStream_Write(void* self, const void * data, uint32_t size, uint32_t * processed_size);
HRESULT WINAPI FFI7Z_Py_IOutStream_Seek(void* self, int64_t offset, uint32_t seekOrigin, uint64_t * newPosition);
HRESULT WINAPI FFI7Z_Py_IProgress_SetTotal(void* self, uint64_t total);
HRESULT WINAPI FFI7Z_Py_IProgress_SetCompleted(void* self, const uint64_t * complete_value);
HRESULT WINAPI FFI7Z_Py_IArchiveExtractCallback_GetStream(void* self, uint32_t index, FFI7Z_ISequentialOutStream * out_stream, int32_t ask_extract_mode);
HRESULT WINAPI FFI7Z_Py_IArchiveExtractCallback_PrepareOperation(void* self, int32_t ask_extract_mode);
HRESULT WINAPI FFI7Z_Py_IArchiveExtractCallback_SetOperationResult(void* self, int32_t op_result);
HRESULT WINAPI FFI7Z_Py_IArchiveOpenCallback_SetTotal(void* self, const uint64_t * files, const uint64_t * bytes);
HRESULT WINAPI FFI7Z_Py_IArchiveOpenCallback_SetCompleted(void* self, const uint64_t * files, const uint64_t * bytes);
HRESULT WINAPI FFI7Z_Py_IArchiveOpenSetSubArchiveName_SetSubArchiveName(void* self, const wchar_t * name);
HRESULT WINAPI FFI7Z_Py_IArchiveOpenVolumeCallback_GetProperty(void* self, PROPID prop_id, PROPVARIANT * value);
HRESULT WINAPI FFI7Z_Py_IArchiveOpenVolumeCallback_GetStream(void* self, const wchar_t * name, FFI7Z_IInStream ** in_stream);
HRESULT WINAPI FFI7Z_Py_ICompressCodecsInfo_GetNumMethods(void* self, uint32_t * num_methods);
HRESULT WINAPI FFI7Z_Py_ICompressCodecsInfo_GetProperty(void* self, uint32_t index, PROPID prop_id, PROPVARIANT * value);
HRESULT WINAPI FFI7Z_Py_ICompressCodecsInfo_CreateDecoder(void* self, uint32_t index, const GUID * iid, void ** coder);
HRESULT WINAPI FFI7Z_Py_ICompressCodecsInfo_CreateEncoder(void* self, uint32_t index, const GUID * iid, void ** coder);
HRESULT WINAPI FFI7Z_Py_ICompressProgressInfo_SetRatioInfo(void* self, const uint64_t * in_size, const uint64_t * out_size);
HRESULT WINAPI FFI7Z_Py_ICryptoGetTextPassword_CryptoGetTextPassword(void* self, wchar_t ** password);
HRESULT WINAPI FFI7Z_Py_ICryptoGetTextPassword2_CryptoGetTextPassword2(void* self, int32_t * password_is_defined, wchar_t ** password);
HRESULT WINAPI FFI7Z_Py_IInArchive_Open(void* self, FFI7Z_IInStream * stream, const uint64_t * max_check_start_position, FFI7Z_IArchiveOpenCallback * open_callback);
HRESULT WINAPI FFI7Z_Py_IInArchive_Close(void* self);
HRESULT WINAPI FFI7Z_Py_IInArchive_GetNumberOfItems(void* self, uint32_t * num_items);
HRESULT WINAPI FFI7Z_Py_IInArchive_GetProperty(void* self, uint32_t index, PROPID prop_id, PROPVARIANT * value);
HRESULT WINAPI FFI7Z_Py_IInArchive_Extract(void* self, const uint32_t * indices, uint32_t num_items, int32_t test_mode, FFI7Z_IArchiveExtractCallback * extract_callback);
HRESULT WINAPI FFI7Z_Py_IInArchive_GetArchiveProperty(void* self, PROPID prop_id, PROPVARIANT * value);
HRESULT WINAPI FFI7Z_Py_IInArchive_GetNumberOfProperties(void* self, uint32_t * num_props);
HRESULT WINAPI FFI7Z_Py_IInArchive_GetPropertyInfo(void* self, uint32_t index, wchar_t ** name, PROPID * prop_id, VARTYPE * var_type);
HRESULT WINAPI FFI7Z_Py_IInArchive_GetNumberOfArchiveProperties(void* self, uint32_t * num_properties);
HRESULT WINAPI FFI7Z_Py_IInArchive_GetArchivePropertyInfo(void* self, uint32_t index, wchar_t ** name, PROPID * prop_id, VARTYPE * var_type);
HRESULT WINAPI FFI7Z_Py_ISetCompressCodecsInfo_SetCompressCodecsInfo(void* self, FFI7Z_ICompressCodecsInfo * compress_codecs_info);

const GUID FFI7Z_IID_IUnknown = { 0x00000000, 0x0000, 0x0000, { 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x46 } };

const FFI7Z_IUnknown_vtable FFI7Z_PyIUnknown_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
};

const GUID FFI7Z_IID_ISequentialInStream = { 0x23170f69, 0x40c1, 0x278a, { 0x00, 0x00, 0x00, 0x03, 0x00, 0x01, 0x00, 0x00 } };

const FFI7Z_ISequentialInStream_vtable FFI7Z_PyISequentialInStream_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
  .Read = FFI7Z_Py_ISequentialInStream_Read,
};

const GUID FFI7Z_IID_IInStream = { 0x23170f69, 0x40c1, 0x278a, { 0x00, 0x00, 0x00, 0x03, 0x00, 0x03, 0x00, 0x00 } };

const FFI7Z_IInStream_vtable FFI7Z_PyIInStream_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
  .Read = FFI7Z_Py_ISequentialInStream_Read,
  .Seek = FFI7Z_Py_IInStream_Seek,
};

const GUID FFI7Z_IID_ISequentialOutStream = { 0x23170f69, 0x40c1, 0x278a, { 0x00, 0x00, 0x00, 0x03, 0x00, 0x02, 0x00, 0x00 } };

const FFI7Z_ISequentialOutStream_vtable FFI7Z_PyISequentialOutStream_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
  .Write = FFI7Z_Py_ISequentialOutStream_Write,
};

const GUID FFI7Z_IID_IOutStream = { 0x23170f69, 0x40c1, 0x278a, { 0x00, 0x00, 0x00, 0x03, 0x00, 0x05, 0x00, 0x00 } };

const FFI7Z_IOutStream_vtable FFI7Z_PyIOutStream_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
  .Write = FFI7Z_Py_ISequentialOutStream_Write,
  .Seek = FFI7Z_Py_IOutStream_Seek,
};

const GUID FFI7Z_IID_IProgress = { 0x23170f69, 0x40c1, 0x278a, { 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00 } };

const FFI7Z_IProgress_vtable FFI7Z_PyIProgress_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
  .SetTotal = FFI7Z_Py_IProgress_SetTotal,
  .SetCompleted = FFI7Z_Py_IProgress_SetCompleted,
};

const GUID FFI7Z_IID_IArchiveExtractCallback = { 0x23170f69, 0x40c1, 0x278a, { 0x00, 0x00, 0x00, 0x06, 0x00, 0x20, 0x00, 0x00 } };

const FFI7Z_IArchiveExtractCallback_vtable FFI7Z_PyIArchiveExtractCallback_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
  .SetTotal = FFI7Z_Py_IProgress_SetTotal,
  .SetCompleted = FFI7Z_Py_IProgress_SetCompleted,
  .GetStream = FFI7Z_Py_IArchiveExtractCallback_GetStream,
  .PrepareOperation = FFI7Z_Py_IArchiveExtractCallback_PrepareOperation,
  .SetOperationResult = FFI7Z_Py_IArchiveExtractCallback_SetOperationResult,
};

const GUID FFI7Z_IID_IArchiveOpenCallback = { 0x23170f69, 0x40c1, 0x278a, { 0x00, 0x00, 0x00, 0x06, 0x00, 0x10, 0x00, 0x00 } };

const FFI7Z_IArchiveOpenCallback_vtable FFI7Z_PyIArchiveOpenCallback_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
  .SetTotal = FFI7Z_Py_IArchiveOpenCallback_SetTotal,
  .SetCompleted = FFI7Z_Py_IArchiveOpenCallback_SetCompleted,
};

const GUID FFI7Z_IID_IArchiveOpenSetSubArchiveName = { 0x23170f69, 0x40c1, 0x278a, { 0x00, 0x00, 0x00, 0x06, 0x00, 0x50, 0x00, 0x00 } };

const FFI7Z_IArchiveOpenSetSubArchiveName_vtable FFI7Z_PyIArchiveOpenSetSubArchiveName_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
  .SetSubArchiveName = FFI7Z_Py_IArchiveOpenSetSubArchiveName_SetSubArchiveName,
};

const GUID FFI7Z_IID_IArchiveOpenVolumeCallback = { 0x23170f69, 0x40c1, 0x278a, { 0x00, 0x00, 0x00, 0x06, 0x00, 0x30, 0x00, 0x00 } };

const FFI7Z_IArchiveOpenVolumeCallback_vtable FFI7Z_PyIArchiveOpenVolumeCallback_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
  .GetProperty = FFI7Z_Py_IArchiveOpenVolumeCallback_GetProperty,
  .GetStream = FFI7Z_Py_IArchiveOpenVolumeCallback_GetStream,
};

const GUID FFI7Z_IID_ICompressCodecsInfo = { 0x23170f69, 0x40c1, 0x278a, { 0x00, 0x00, 0x00, 0x04, 0x00, 0x60, 0x00, 0x00 } };

const FFI7Z_ICompressCodecsInfo_vtable FFI7Z_PyICompressCodecsInfo_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
  .GetNumMethods = FFI7Z_Py_ICompressCodecsInfo_GetNumMethods,
  .GetProperty = FFI7Z_Py_ICompressCodecsInfo_GetProperty,
  .CreateDecoder = FFI7Z_Py_ICompressCodecsInfo_CreateDecoder,
  .CreateEncoder = FFI7Z_Py_ICompressCodecsInfo_CreateEncoder,
};

const GUID FFI7Z_IID_ICompressProgressInfo = { 0x23170f69, 0x40c1, 0x278a, { 0x00, 0x00, 0x00, 0x04, 0x00, 0x04, 0x00, 0x00 } };

const FFI7Z_ICompressProgressInfo_vtable FFI7Z_PyICompressProgressInfo_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
  .SetRatioInfo = FFI7Z_Py_ICompressProgressInfo_SetRatioInfo,
};

const GUID FFI7Z_IID_ICryptoGetTextPassword = { 0x23170f69, 0x40c1, 0x278a, { 0x00, 0x00, 0x00, 0x05, 0x00, 0x10, 0x00, 0x00 } };

const FFI7Z_ICryptoGetTextPassword_vtable FFI7Z_PyICryptoGetTextPassword_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
  .CryptoGetTextPassword = FFI7Z_Py_ICryptoGetTextPassword_CryptoGetTextPassword,
};

const GUID FFI7Z_IID_ICryptoGetTextPassword2 = { 0x23170f69, 0x40c1, 0x278a, { 0x00, 0x00, 0x00, 0x05, 0x00, 0x11, 0x00, 0x00 } };

const FFI7Z_ICryptoGetTextPassword2_vtable FFI7Z_PyICryptoGetTextPassword2_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
  .CryptoGetTextPassword2 = FFI7Z_Py_ICryptoGetTextPassword2_CryptoGetTextPassword2,
};

const GUID FFI7Z_IID_IInArchive = { 0x23170f69, 0x40c1, 0x278a, { 0x00, 0x00, 0x00, 0x06, 0x00, 0x60, 0x00, 0x00 } };

const FFI7Z_IInArchive_vtable FFI7Z_PyIInArchive_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
  .Open = FFI7Z_Py_IInArchive_Open,
  .Close = FFI7Z_Py_IInArchive_Close,
  .GetNumberOfItems = FFI7Z_Py_IInArchive_GetNumberOfItems,
  .GetProperty = FFI7Z_Py_IInArchive_GetProperty,
  .Extract = FFI7Z_Py_IInArchive_Extract,
  .GetArchiveProperty = FFI7Z_Py_IInArchive_GetArchiveProperty,
  .GetNumberOfProperties = FFI7Z_Py_IInArchive_GetNumberOfProperties,
  .GetPropertyInfo = FFI7Z_Py_IInArchive_GetPropertyInfo,
  .GetNumberOfArchiveProperties = FFI7Z_Py_IInArchive_GetNumberOfArchiveProperties,
  .GetArchivePropertyInfo = FFI7Z_Py_IInArchive_GetArchivePropertyInfo,
};

const GUID FFI7Z_IID_ISetCompressCodecsInfo = { 0x23170f69, 0x40c1, 0x278a, { 0x00, 0x00, 0x00, 0x40, 0x00, 0x61, 0x00, 0x00 } };

const FFI7Z_ISetCompressCodecsInfo_vtable FFI7Z_PyISetCompressCodecsInfo_vtable = {
  .QueryInterface = FFI7Z_Py_IUnknown_QueryInterface,
  .AddRef = FFI7Z_Py_IUnknown_AddRef,
  .Release = FFI7Z_Py_IUnknown_Release,
  .SetCompressCodecsInfo = FFI7Z_Py_ISetCompressCodecsInfo_SetCompressCodecsInfo,
};

/* - END GENERATED CIMPL - */
