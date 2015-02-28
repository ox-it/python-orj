from ..enums import ObjectType
from .. import spatial
from ..utils import *

from .entity import Entity

class Polyline(Entity):
    object_type = ObjectType.POLYLINE

    def read(self, f, ht):
        object_version = read_int(f)
        if object_version > 1:
            raise AssertionError
        super(Polyline, self).read(f)
        self.geometry = spatial.read_polyline_3d(f)

