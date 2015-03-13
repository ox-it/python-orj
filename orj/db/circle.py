from ..enums import ObjectType
from .. import spatial
from ..utils import *

from .entity import Entity

class Circle(Entity):
    object_type = ObjectType.CIRCLE

    def read(self, f, ht):
        object_version = read_int(f)
        if object_version > 1:
            raise AssertionError
        super(Circle, self).read(f)
        self.geometry = spatial.Circle3D(spatial.read_point_3d(f), read_double(f))

