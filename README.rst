python-lib7zip
==============
Python bindings for lib7zip_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:author: Mark Harviston <mark.harviston@gmail.com>

This project is a Work-in-Progress and currently going through a rigorous
valgrinding process to eliminate memory leaks and segmentation faults.

pylib7zip is a binding for the c++ api lib7zip which is in turn a wrapper over
7z.so/7z.dll which is a C API that uses Windows COM+ conventions (and written
in C\++)

Dependencies
------------

    * 7z.so/7z.dll from http://7zip.org or p7zip on \*Nix
    * my fork_ of lib7zip_ available on bitbucket
    * libc7zip has been moved to my fork of lib7zip
    * CFFI_

How To Use
----------

See pytests.py for an example, currently only getting (some) info from archives
is supported CFFI.

so far, CFFI seems somewhat, but not drastically easier to use, but also
somewhat slower than ctypes, but it shouldn't be, so there's probably something
wrong with my code?

(not that the pylib7zip.cpp was ever really "done").

License
-------

This code is licensed under the BSD 2-clause license.

However, lib7zip is licensed under the MPL and 7zip itself (7z.so/7z.dll) is
licensed under the LGPL (with extra restrictions on the code the handles rar
files).

This shouldn't be a problem since by default all these components are
dynamically linked by default. The MPL allows static linking with non-mpl code
(even proprietary fcode), so staticly linking lib7zip and pylib7zip together is
possible (and potentially the best course of action for many projects).

.. _CFFI: https://cffi.readthedocs.org/en/release-0.6/
.. _fork: http://bitbucket.org/infinull/lib7zip
.. _lib7ip: http://code.google.com/p/lib7zip/
