# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class FileinfoFi(KaitaiStruct):
    """fileinfo.fi files store detailed file description alongside file names
    that are displayed by the fi.exe program. This format was used by Norton
    Utilities 4 on MS-DOS systems.
    
    .. seealso::
       Source - https://en.wikipedia.org/wiki/Norton_Utilities
    """
    def __init__(self, _io, _parent=None, _root=None):
        super(FileinfoFi, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.header = FileinfoFi.Header(self._io, self, self._root)
        self.records = []
        for i in range(self.header.num_records):
            self.records.append(FileinfoFi.Record(self._io, self, self._root))



    def _fetch_instances(self):
        pass
        self.header._fetch_instances()
        for i in range(len(self.records)):
            pass
            self.records[i]._fetch_instances()


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(FileinfoFi.Header, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(5)
            if not self.magic == b"\x50\x4E\x43\x49\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x50\x4E\x43\x49\x00", self.magic, self._io, u"/types/header/seq/0")
            self.num_records = self._io.read_u2le()
            self.checksum = self._io.read_u2le()
            self.bitmask = self._io.read_bytes(128)


        def _fetch_instances(self):
            pass


    class Record(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(FileinfoFi.Record, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.file_name = (KaitaiStream.bytes_terminate(self._io.read_bytes(12), 0, False)).decode(u"IBM437")
            self.comment = KaitaiStream.bytes_terminate(self._io.read_bytes(65), 0, False)


        def _fetch_instances(self):
            pass



