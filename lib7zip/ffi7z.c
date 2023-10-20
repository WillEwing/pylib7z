#define NOMINMAX
#define WIN32_LEAN_AND_MEAN
#include <PropIdlBase.h>
#include <Windows.h>
#include <stdint.h>

#include <stdio.h>

/* Library Interface */

typedef HRESULT(WINAPI *FFI7Z_PFN_CreateObject)(const GUID *clsID, const GUID *iid, void **outObject);
typedef HRESULT(WINAPI *FFI7Z_PFN_GetNumberOfFormats)(uint32_t *numFormats);
typedef HRESULT(WINAPI *FFI7Z_PFN_GetHandlerProperty2)(uint32_t index, PROPID propID, PROPVARIANT *value);
typedef HRESULT(WINAPI *FFI7Z_PFN_GetNumberOfMethods)(uint32_t *numMethods);
typedef HRESULT(WINAPI *FFI7Z_PFN_GetMethodProperty)(uint32_t index, PROPID propID, PROPVARIANT *value);

typedef struct FFI7Z_INTFtag
{
    HMODULE h7ZDLL;
    FFI7Z_PFN_CreateObject CreateObject;
    FFI7Z_PFN_GetNumberOfFormats GetNumberOfFormats;
    FFI7Z_PFN_GetHandlerProperty2 GetHandlerProperty2;
    FFI7Z_PFN_GetNumberOfMethods GetNumberOfMethods;
    FFI7Z_PFN_GetMethodProperty GetMethodProperty;
} FFI7Z_INTF;

static FFI7Z_INTF sFFI7ZIntf;

HRESULT InitModule(const wchar_t *lib7zip_path)
{
    HMODULE h7ZDLL = LoadLibraryW(lib7zip_path);
    if (h7ZDLL == NULL)
    {
        DWORD last_error = GetLastError();
        return HRESULT_FROM_WIN32(last_error);
    }

#define FFI7Z_LOAD_PROC_ADDR(proc_name)                                                                                \
    do                                                                                                                 \
    {                                                                                                                  \
        FFI7Z_PFN_##proc_name proc_addr = (FFI7Z_PFN_##proc_name)GetProcAddress(h7ZDLL, #proc_name);                   \
        if (proc_addr == NULL)                                                                                         \
        {                                                                                                              \
            DWORD last_error = GetLastError();                                                                         \
            return HRESULT_FROM_WIN32(last_error);                                                                     \
        }                                                                                                              \
        intf.proc_name = proc_addr;                                                                                    \
    } while (0)

    FFI7Z_INTF intf;
    ZeroMemory(&intf, sizeof(FFI7Z_INTF));
    intf.h7ZDLL = h7ZDLL;
    FFI7Z_LOAD_PROC_ADDR(CreateObject);
    FFI7Z_LOAD_PROC_ADDR(GetNumberOfFormats);
    FFI7Z_LOAD_PROC_ADDR(GetHandlerProperty2);
    FFI7Z_LOAD_PROC_ADDR(GetNumberOfMethods);
    FFI7Z_LOAD_PROC_ADDR(GetMethodProperty);
    MoveMemory(&sFFI7ZIntf, &intf, sizeof(FFI7Z_INTF));
    return S_OK;

#undef FFI7Z_LOAD_PROC_ADDR
}

HRESULT CreateObject(const GUID *clsid, const GUID *iid, void **out_object)
{
    if (sFFI7ZIntf.CreateObject == NULL)
    {
        return E_NOTIMPL;
    }

    return sFFI7ZIntf.CreateObject(clsid, iid, out_object);
}

HRESULT GetNumberOfFormats(uint32_t *num_formats)
{
    if (sFFI7ZIntf.GetNumberOfFormats == NULL)
    {
        return E_NOTIMPL;
    }

    return sFFI7ZIntf.GetNumberOfFormats(num_formats);
}

HRESULT GetHandlerProperty2(uint32_t index, PROPID prop_id, PROPVARIANT *value)
{
    if (sFFI7ZIntf.GetHandlerProperty2 == NULL)
    {
        return E_NOTIMPL;
    }

    return sFFI7ZIntf.GetHandlerProperty2(index, prop_id, value);
}

HRESULT GetNumberOfMethods(uint32_t *num_methods)
{
    if (sFFI7ZIntf.GetNumberOfMethods == NULL)
    {
        return E_NOTIMPL;
    }

    return sFFI7ZIntf.GetNumberOfMethods(num_methods);
}

HRESULT GetMethodProperty(uint32_t index, PROPID prop_id, PROPVARIANT *value)
{
    if (sFFI7ZIntf.GetMethodProperty == NULL)
    {
        return E_NOTIMPL;
    }

    return sFFI7ZIntf.GetMethodProperty(index, prop_id, value);
}

/* Type Helpers */

PROPVARIANT *CreatePropVariant()
{
    PROPVARIANT *pvar = (PROPVARIANT *)HeapAlloc(GetProcessHeap(), 0, sizeof(PROPVARIANT));
    if (pvar)
    {
        PropVariantInit(pvar);
    }
    return pvar;
}

void DeletePropVariant(PROPVARIANT *pvar)
{
    if (pvar)
    {
        PropVariantClear(pvar);
        HeapFree(GetProcessHeap(), 0, pvar);
    }
}
