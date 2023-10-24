python-lib7zip
==============

Python bindings for 7-Zip
~~~~~~~~~~~~~~~~~~~~~~~~~
:author: William Ewing <will.ewing.iv@gmail.com>
:author: Mark Harviston <mark.harviston@gmail.com>
:version: 0.2

pylib7zip is a direct binding to 7z.dll from the 7-zip project (7zip.org)

7z.dll uses Windows COM+ calling conventions without registering itself with the COM server
and has an over-engineered slightly pathological OOP API.

Only reading metadata and extracting files is currently supported.
The library currently relies on on Windows API for memory allocation/deallocation.


Dependencies
------------

    * 7z.dll from 7-zip_
    * CFFI_
    * ast-compat_ on python versions prior to 3.12

How To Use
----------
By default the path to 7z.dll/7z.so will be autodetected.

.. code:: python

	from lib7zip import Archive, formats

	#view information on supported formats
	for format in formats:
		print(format.name, ', '.join(format.extensions))

	#type of archive will be autodetected
	#pass in optional forceformat argument to force the use a particular format (use the name)
	#pass in optional password argument to open encrypted archives.
	with Archive('path_to.7z') as archive:
		#extract all items to the directory, directory will be created if it doesn't exist
		archive.extract('extract_here')

		#list all items in the archive and get their metadata
		for item in archive:
			print( item.isdir, item.path, item.crc)

		# extract items that match certain criteria
		def filter_items(items):
			for item in items:
				if item.path.endswith('.txt'):
					yield item

		archive.extract('extract_some_here', filter_items(archive))

		#extract a particular archive item to a python stream object
		data = archive[0].read_bytes()  # a bytes object containing the contents of item 0
		text = archive[0].read_text(encoding='utf-8')  # a str object containing the contents of item 3

License
-------

This code is licensed under the BSD 2-clause license.

7-Zip is available under the LGPL with the exception of the code handling rar compression.

.. _7-zip: https://7-zip.org
.. _CFFI: https://cffi.readthedocs.io/en/stable/
.. _ast-compat: https://github.com/python-compiler-tools/ast-compat/
