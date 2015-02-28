from ..enums import ObjectType
from ..utils import *

from .group import Group

class SymbolDef(Group):
    object_type = ObjectType.SYMBOL_DEF

    def read(self, f, ht):
        object_version = read_int(f)
        if object_version > 1:
            raise AssertionError
        super(SymbolDef, self).read(f, ht)
        self.name = read_string(f)

