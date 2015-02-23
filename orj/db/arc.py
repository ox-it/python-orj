from ..enums import ObjectType
from .. import spatial
from ..utils import *

from .entity import Entity

class Arc(Entity):
    object_type = ObjectType.ARC

    def read(self, f, ht):
        object_version = read_int(f)
        if object_version > 1:
            raise AssertionError
        super(Arc, self).read(f)

        self.geometry = spatial.Arc3D(center=spatial.read_point_3d(f),
                                      radius=read_double(f),
                                      start_angle=read_double(f),
                                      angle=read_double(f))

