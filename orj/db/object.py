import struct

from ..enums import AttributeType
from ..utils import *

class Object(object):
    def __init__(self):
        self.attributes = {}

    def read_object_version(self, f):
        return read_int(f)

    def read(self, f):
        object_version = read_int(f)
        if object_version > 3:
            raise NotImplementedError
        self.object_id = read_long(f)
        if object_version >= 2:
            for i in range(read_int(f)):
                try:
                    attribute_type = AttributeType(read_byte(f))
                except ValueError:
                    object_type = f.read(read_int(f))
                    obj = Object.create(object_type)
                else:
                    from .attribute import Attribute
                    obj = Attribute.create(attribute_type)
                if obj:
                    obj.read(f)
                if isinstance(obj, Attribute):
                    self.attributes[obj.name] = obj

    @classmethod
    def create(cls, object_type):
        from . import registry
        return registry[object_type]()
