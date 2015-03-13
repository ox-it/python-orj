from ..enums import ObjectType
from .. import spatial
from ..utils import *

from .entity import Entity

class Polygon(Entity):
    object_type = ObjectType.POLYGON

    def read(self, f, ht):
        object_version = read_int(f)
        if object_version > 2:
            raise AssertionError
        super(Polygon, self).read(f)
        if object_version >= 2:
            self.geometry = spatial.read_polygon_3d_with_bulges(f)
        else:
            self.geometry = spatial.read_polygon_3d(f)
        assert f.pos == f.len

