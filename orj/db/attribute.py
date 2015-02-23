from ..enums import AttributeType
from ..utils import *

from .object import Object

class Attribute(Object):
    def read(self, f):
        object_version = read_int(f)
        if object_version > 3:
            raise NotImplementedError
        super(Attribute, self).read(f)
        self.name = read_string(f)

    @classmethod
    def create(cls, attribute_type):
        return attribute_registry[attribute_type]()

class AttributeString(Attribute):
    def read(self, f):
        object_version = read_int(f)
        if object_version > 1:
            raise NotImplementedError
        super(AttributeString, self).read(f)
        self.value = read_string(f)
        self.description = read_string(f)
        return 0

    def __unicode__(self):
        return "Attribute(%r, %r)" % (self.name, self.value)
    __repr__ = __str__ = __unicode__

attribute_registry = {
    AttributeType.STRING: AttributeString,
}
