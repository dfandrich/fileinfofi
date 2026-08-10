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
# CP437 (a.k.a. IBM437) is a good default because 1) it's common (the U.S.A.
# default), and 2) it has a mapping for all 256 octets, so the conversion will
# never fail with UnicodeDecodeError.
DEFAULT_ENCODING = 'CP437'


def fileinfofidump(fn: str, lower: bool, encoding: str) -> int:
    """Dump the contents of the given fileinfo.fi file."""
    try:
        fi = fileinfo_fi.FileinfoFi.from_file(fn)
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

    if fi.header_checksum != fi.header.checksum:
        print('Error: file failed checksum validation', file=sys.stderr)
        return 1

    for i, f in enumerate(fi.records):
        if fi.header.record_in_use[i]:
            file_name = f.file_name if not lower else f.file_name.lower()
            try:
                print(file_name, f.comment.decode(encoding))
            except LookupError:
                print('Error: unknown encoding', encoding, file=sys.stderr)
                return 1
            except UnicodeDecodeError:
                print('Error: comment contains a character that cannot be '
                      'expressed in the encoding', encoding, file=sys.stderr)
                return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Output contents of a fileinfo.fi file')
    _ = parser.add_argument(
        '-e', metavar='ENCODING', default=DEFAULT_ENCODING,
        help=f'Character encoding of fileinfo.fi file (default: {DEFAULT_ENCODING})'
    )
    _ = parser.add_argument('-l', action='store_true', help='output file names in lower case')
    _ = parser.add_argument('files', nargs='*', help='paths to fileinfo.fi file(s)',
                            default=['fileinfo.fi'])
    args = parser.parse_args(args=argv)
    rc = 0
    for fn in args.files:
        rc |= fileinfofidump(fn, args.l, args.e)
    return rc


if __name__ == '__main__':
    sys.exit(main())
