"""Displays the contents of a fileinfo.fi file.

This file type is created by the Norton Utilities 4 fi.exe program on MS-DOS to
hold extended file comments for DOS 8.3 file names.

fileinfo_fi.py is created with the command:
    kaitai-struct-compiler -t python fileinfo_fi.ksy

Hopefully, the .ksy file will eventually end up in
https://github.com/kaitai-io/kaitai_struct_formats
"""

from __future__ import annotations

import argparse
import sys

import fileinfo_fi

import kaitaistruct

# The code page in use when the file descriptions were created.
# Change this if the code page being used was something else.
DEFAULT_ENCODING = 'IBM437'


class FileinfoFiEx(fileinfo_fi.FileinfoFi):
    """FileinfoFi parser with extra methods."""

    def validate_header_checksum(self) -> bool:
        """Validate that the header checksum is correct."""
        # Must reconstitute the original integers to calculate the header checksum
        bitmask_sum = sum(2 ** (7 - (i % 8)) for i, v in enumerate(self.header.record_in_use) if v)
        checksum = (
            sum(self.header.magic)
            + (self.header.num_records >> 8) + (self.header.num_records % 256)
            + bitmask_sum
        )
        return checksum == self.header.checksum


def fileinfofidump(fn: str, lower: bool = False) -> int:
    """Dump the contents of the given fileinfo.fi file."""
    try:
        fi = FileinfoFiEx.from_file(fn)
    except OSError as e:
        print(f'{type(e).__name__}: {e!s}', file=sys.stderr)
        return 1
    except kaitaistruct.ValidationNotEqualError:
        print('Error: file does not appear to be in fileinfo.fi format (wrong magic)',
              file=sys.stderr)
        return 1
    except kaitaistruct.EndOfStreamError:
        print('Error: file does not appear to be in fileinfo.fi format (too short)',
              file=sys.stderr)
        return 1

    if not fi.validate_header_checksum():
        print('Error: file failed checksum validation', file=sys.stderr)
        return 1

    for i, f in enumerate(fi.records):
        if fi.header.record_in_use[i]:
            file_name = f.file_name if not lower else f.file_name.lower()
            print(file_name, f.comment.decode(DEFAULT_ENCODING))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Output contents of a fileinfo.fi file')
    _ = parser.add_argument('-l', action='store_true', help='output file names in lower case')
    _ = parser.add_argument('files', nargs='*', help='paths to fileinfo.fi file(s)',
                            default=['fileinfo.fi'])
    args = parser.parse_args(args=argv)
    rc = 0
    for fn in args.files:
        rc = rc ^ fileinfofidump(fn, args.l)
    return rc


if __name__ == '__main__':
    sys.exit(main())
