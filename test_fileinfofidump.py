"""Test fileinfofidump."""

import contextlib
import io
import textwrap
import unittest
from unittest import mock

import fileinfofidump


class TestFileinfofidump(unittest.TestCase):
    """Test fileinfofidump.main."""

    def test_fileinfofidump(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            rc = fileinfofidump.main([])

        self.assertEqual(0, rc)
        self.assertEqual(textwrap.dedent("""\
                            README.MD Introductory information about fileinfofi
                            LICENSE MIT License
                            FILEINFO.FI File storing all the comments you're reading now
                         """),
                         output.getvalue())

    def test_fileinfofidump_lower(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            rc = fileinfofidump.main(['-l'])

        self.assertEqual(0, rc)
        self.assertEqual(textwrap.dedent("""\
                             readme.md Introductory information about fileinfofi
                             license MIT License
                             fileinfo.fi File storing all the comments you're reading now
                         """),
                         output.getvalue())

    def test_fileinfofidump_missingfile(self):
        self.assertEqual(1, fileinfofidump.main(["file/that/doesn't/exist"]))

    def test_fileinfofidump_badfile(self):
        self.assertEqual(1, fileinfofidump.main(['README.md']))

    @mock.patch('kaitaistruct.open', mock.mock_open(read_data=b'PNCI'))
    def test_fileinfofidump_shortfile(self):
        self.assertEqual(1, fileinfofidump.main(['mock-fileinfo.fi']))

    @mock.patch('kaitaistruct.open', mock.mock_open(read_data=b'PNCI' + b'\x00' * 200))
    def test_fileinfofidump_badchecksum(self):
        self.assertEqual(1, fileinfofidump.main(['mock-fileinfo.fi']))
