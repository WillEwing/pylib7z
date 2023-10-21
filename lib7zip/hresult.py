#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import IntEnum


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
