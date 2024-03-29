from ..enums import ObjectType
from orj.spatial import creation
from ..utils import *

from .entity import Entity
from .. import spatial

class Arc(Entity):
    object_type = ObjectType.ARC

    def read(self, f, ht):
        object_version = read_int(f)
        if object_version > 1:
            raise AssertionError
        super(Arc, self).read(f)

        self.geometry = spatial.create_arc(f)

