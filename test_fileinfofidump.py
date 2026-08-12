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
        self.assertMultiLineEqual(textwrap.dedent("""\
            README.MD Introductory information about fileinfofi
            LICENSE MIT License
            FILEINFO.FI File storing all the comments you're reading now
            """), output.getvalue())

    def test_fileinfofidump_lower(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            rc = fileinfofidump.main(['-l'])

        self.assertEqual(0, rc)
        self.assertMultiLineEqual(textwrap.dedent("""\
            readme.md Introductory information about fileinfofi
            license MIT License
            fileinfo.fi File storing all the comments you're reading now
            """), output.getvalue())

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

    def test_fileinfofidump_large(self):
        """Test the largest real fileinfo.fi file."""
        with contextlib.redirect_stdout(io.StringIO()) as output:
            rc = fileinfofidump.main(['fileinfo-test.fi'])
        res = output.getvalue()

        self.assertEqual(0, rc)
        # The output is very long so just check that it starts and ends
        # correctly
        self.assertEqual(12161, len(res))
        self.assertTrue(res.startswith(textwrap.dedent("""\
            1 This is the largest file created by Norton Utilities.
            2 Here are some high-bit characters: ░▒▓
            3 File is 3
            """)))
        self.assertTrue(res.endswith(textwrap.dedent("""\
            767 File is 767
            768 File is 768
            769 File is 769
            """)))

    def test_fileinfofidump_encoding(self):
        """Test the -e flag to set the character encoding."""
        with contextlib.redirect_stdout(io.StringIO()) as output:
            rc = fileinfofidump.main(['-e', 'iso-8859-1', 'fileinfo-test.fi'])
        res = output.getvalue()

        self.assertEqual(0, rc)
        # The output is very long so just check that it starts and ends
        # correctly
        self.assertEqual(12161, len(res))
        self.assertTrue(res.startswith(textwrap.dedent("""\
            1 This is the largest file created by Norton Utilities.
            2 Here are some high-bit characters: °±²
            3 File is 3
            """)))
        self.assertTrue(res.endswith(textwrap.dedent("""\
            767 File is 767
            768 File is 768
            769 File is 769
            """)))

    def test_fileinfofidump_invalid_encoding(self):
        """Select an invalid encoding with the -e flag."""
        with contextlib.redirect_stdout(io.StringIO()) as output:
            rc = fileinfofidump.main(['-e', 'not-a-valid-encoding'])
        res = output.getvalue()

        self.assertEqual(1, rc)
        self.assertEqual('', res)

    def test_fileinfofidump_insufficient_encoding(self):
        """Select an encoding that won't work for the comments."""
        with contextlib.redirect_stdout(io.StringIO()) as output:
            rc = fileinfofidump.main(['-e', 'us-ascii', 'fileinfo-test.fi'])
        res = output.getvalue()

        self.assertEqual(1, rc)
        self.assertEqual('1 This is the largest file created by Norton Utilities.\n', res)
