import StringIO

from ..enums import Units, AttributeType
from ..utils import *

from .object import Object
from .attribute import Attribute

class DatabaseHeader(Object):
    def read(self, f):
        object_version = self.read_object_version(f)
        if object_version > 4:
            raise AssertionError

        self.new_object_id = read_long(f)
        self.fill_space = read_bool(f)
        self.ortho_mode = read_bool(f)
        self.snap_mode = read_bool(f)
        self.auto_space = read_bool(f)
        i = read_int(f)
        self.dxf_import_pline_to_space = read_bool(f)
        self.units = Units(read_int(f))

        j = read_int(f)
        self.odbc_databases = [read_string(f) for x in range(j)]

        if i >= 2:
            self.some_int = read_int(f)
        if i >= 3:
            self.some_string = read_string(f)
        if i >= 4:

            self.attributes = []
            for x in range(read_int(f)):
                attribute_type = read_byte(f)
                try:
                    attribute_type = AttributeType(attribute_type)
                except ValueError:
                    raise NotImplementedError
                else:
                    attribute = Attribute.create(attribute_type)
                    attribute.read(f)
                    self.attributes.append(attribute)

        assert not f.read(1) # Make sure we've consumed the entire buffer
