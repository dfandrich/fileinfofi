"""Displays the contents of a fileinfo.fi file.

This file type is created by the Norton Utilities 4 fi.exe program on MS-DOS to
hold extended file comments for DOS 8.3 file names.

fileinfo_fi.py is created with the command:
    kaitai-struct-compiler -t python fileinfo_fi.ksy

Hopefully, the .ksy file will eventually end up in
https://github.com/kaitai-io/kaitai_struct_formats
"""

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
        checksum = (
            sum(self.header.magic)
            + (self.header.num_records >> 8) + (self.header.num_records % 256)
            + sum(self.header.bitmask)
        )
        return checksum == self.header.checksum

    def is_record_valid(self, index: int) -> bool:
        """Check if the given record bitmask is marked as valid."""
        bindex = index // 8
        if bindex >= len(self.header.bitmask):
            return False
        return bool(self.header.bitmask[bindex] & 1 << (7 - index % 8))


def fileinfofidump(fn: str) -> int:
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
        if fi.is_record_valid(i):
            print(f.file_name, f.comment.decode(DEFAULT_ENCODING))
    return 0


def main() -> int:
    rc = 0
    for fn in sys.argv[1:] if len(sys.argv) > 1 else ['fileinfo.fi']:
        rc = rc ^ fileinfofidump(fn)
    return rc


if __name__ == '__main__':
    sys.exit(main())
