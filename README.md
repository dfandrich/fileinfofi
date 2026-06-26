# fileinfofi

This is a program that dumps the contents of fileinfo.fi files as created by
Norton Utilities on MS-DOS. The program `fi.exe` was used as an alternative to
`dir` to display a directory listing with comments next to each file. This was
useful to annotate files that were limited by MS-DOS to 12 character file names
(8.3).

`fileinfodump` reads the contents of a fileinfo.fi file in the current
directory (or the file(s) given on the command-line) and displays its contents
in the form:

    FILENAME.EXT comment for file

## Installation

The latest source code can be obtained from
https://github.com/dfandrich/fileinfofi/

The code is written entirely in Python.  Build and install the latest code
from Github with:

  `python -m pip install https://github.com/dfandrich/fileinfofi/archive/refs/heads/master.tar.gz`

The program requires the `kaitaistruct` package. The file parser is built from
the fileinfo.fi definition in the Kaitai Struct repository using the Kaitai
Struct Compiler, but all generated files are included in this repository so
nothing beyond `kaitaistruct` are required to run it.

## Author

Copyright © 2026 Dan Fandrich <dan@coneharvesters.com>
Licensed under the MIT license (see the file [LICENSE](LICENSE) for details).
