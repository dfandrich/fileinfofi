# fileinfofi

This is a program that dumps the contents of fileinfo.fi files as created by
Norton Utilities on MS-DOS. The program `fi.exe` was used on DOS as an
alternative to `dir` to display a directory listing with comments next to each
file. This was useful to annotate files with more details that were otherwise
limited by MS-DOS to just 12 character names (8.3).

## Installation

The latest source code can be obtained from
https://github.com/dfandrich/fileinfofi/

The code is written entirely in Python.  Build and install the latest code
from Github with:

    python -m pip install https://github.com/dfandrich/fileinfofi/archive/refs/heads/master.tar.gz

The program requires the `kaitaistruct` package. The file parser is built from
a fileinfo.fi definition in [Kaitai Struct](https://kaitai.io/) format using
the Kaitai Struct Compiler, but all generated files are included in this
repository so nothing beyond `kaitaistruct` is required to run it.

## Usage

`fileinfofidump` reads the contents of a fileinfo.fi file in the current
directory (or the file(s) given on the command-line) and displays its contents
in the form:

    FILENAME.EXT comment for file

File name on MS-DOS are case insensitive and the names in fileinfo.fi files are
stored in upper case.

To dump the contents of a fileinfo.fi file, run:

    fileinfofidump /path/to/fileinfo.fi

To dump the contents of a fileinfo.fi file in the current directory, just run:

    fileinfofidump

The return status is 0 on success, or nonzero if an error was encountered (such
as a fileinfo.fi file couldn't be found or read).

## Author

Copyright © 2026 Dan Fandrich <dan@coneharvesters.com>
Licensed under the MIT license (see the file [LICENSE](LICENSE) for details).
