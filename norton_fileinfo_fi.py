# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class NortonFileinfoFi(KaitaiStruct):
    """fileinfo.fi files store detailed file description alongside file names
    that are displayed by the fi.exe program. This format was used by [Norton
    Utilities](https://en.wikipedia.org/wiki/Norton_Utilities) 4 on MS-DOS
    systems.
    """
    def __init__(self, _io, _parent=None, _root=None):
        super(NortonFileinfoFi, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.header = NortonFileinfoFi.Header(self._io, self, self._root)
        self.records = []
        for i in range(self.header.num_records):
            self.records.append(NortonFileinfoFi.Record(self._io, self, self._root))



    def _fetch_instances(self):
        pass
        self.header._fetch_instances()
        for i in range(len(self.records)):
            pass
            self.records[i]._fetch_instances()

        _ = self.record_checksum_reduction
        if hasattr(self, '_m_record_checksum_reduction'):
            pass
            for i in range(len(self._m_record_checksum_reduction)):
                pass
                self._m_record_checksum_reduction[i]._fetch_instances()



    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(NortonFileinfoFi.Header, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(5)
            if not self.magic == b"\x50\x4E\x43\x49\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x50\x4E\x43\x49\x00", self.magic, self._io, u"/types/header/seq/0")
            self.num_records = self._io.read_u2le()
            self.checksum = self._io.read_u2le()
            self.record_in_use = []
            for i in range(1024):
                self.record_in_use.append(self._io.read_bits_int_be(1) != 0)



        def _fetch_instances(self):
            pass
            for i in range(len(self.record_in_use)):
                pass



    class Record(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(NortonFileinfoFi.Record, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.file_name = (KaitaiStream.bytes_terminate(self._io.read_bytes(12), 0, False)).decode(u"IBM437")
            self.comment = KaitaiStream.bytes_terminate(self._io.read_bytes(65), 0, False)


        def _fetch_instances(self):
            pass


    class RecordChecksumIter(KaitaiStruct):
        def __init__(self, idx, prev, _io, _parent=None, _root=None):
            super(NortonFileinfoFi.RecordChecksumIter, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.idx = idx
            self.prev = prev
            self._read()

        def _read(self):
            pass


        def _fetch_instances(self):
            pass

        @property
        def res(self):
            """Add one additional checksum byte from the given `record_in_use` bit.
            """
            if hasattr(self, '_m_res'):
                return self._m_res

            self._m_res = self.prev + (int(self._root.header.record_in_use[self.idx]) << 7 - self.idx % 8)
            return getattr(self, '_m_res', None)


    @property
    def calculated_header_checksum(self):
        """Calculate the expected header checksum from the header data. This is the
        value that should be found in `header.checksum` in a valid file.
        """
        if hasattr(self, '_m_calculated_header_checksum'):
            return self._m_calculated_header_checksum

        self._m_calculated_header_checksum = ((((((KaitaiStream.byte_array_index(self.header.magic, 0) + KaitaiStream.byte_array_index(self.header.magic, 1)) + KaitaiStream.byte_array_index(self.header.magic, 2)) + KaitaiStream.byte_array_index(self.header.magic, 3)) + self.header.num_records // 256) + self.header.num_records % 256) + self.record_checksum) % 65536
        return getattr(self, '_m_calculated_header_checksum', None)

    @property
    def record_checksum(self):
        """Partial checksum of `record_in_use` used in calculating
        `calculated_header_checksum`.
        """
        if hasattr(self, '_m_record_checksum'):
            return self._m_record_checksum

        self._m_record_checksum = self.record_checksum_reduction[len(self._root.header.record_in_use) - 1].res
        return getattr(self, '_m_record_checksum', None)

    @property
    def record_checksum_reduction(self):
        """Expression used in calculating `expected_record_checksum.`
        """
        if hasattr(self, '_m_record_checksum_reduction'):
            return self._m_record_checksum_reduction

        self._m_record_checksum_reduction = []
        for i in range(len(self._root.header.record_in_use)):
            self._m_record_checksum_reduction.append(NortonFileinfoFi.RecordChecksumIter(i, (0 if i == 0 else self.record_checksum_reduction[i - 1].res), self._io, self, self._root))

        return getattr(self, '_m_record_checksum_reduction', None)


