from ..enums import ObjectType
from .. import spatial
from ..utils import *

from .entity import Entity

class SymbolRef(Entity):
    object_type = ObjectType.SYMBOL_REF

    def read(self, f, ht):
        object_version = read_int(f)
        if object_version > 2:
            raise AssertionError
        super(SymbolRef, self).read(f)
        self.name = read_string(f)
        self.transform = spatial.create_transform(f)
        if object_version >= 2:
            self.use_symbol_def_color = read_bool(f)


