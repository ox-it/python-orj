from ..enums import ObjectType
from .. import spatial
from ..utils import *

from .entity import Entity

class Ellipse(Entity):
    object_type = ObjectType.ELLIPSE

    def read(self, f, ht):
        object_version = read_int(f)
        if object_version > 1:
            raise AssertionError
        super(Ellipse, self).read(f)
        self.geometry = spatial.create_ellipse(f)

