from ..enums import ObjectType
from .. import spatial
from ..utils import *

from .entity import Entity

# This reads everything, but does nothing with it. Examples we've seen in the
# wild are just logos, which we don't need to reproduce.

class Image(Entity):
    object_type = ObjectType.IMAGE

    def read(self, f, ht):
        object_version = read_int(f)
        if object_version > 3:
            raise AssertionError
        super(Image, self).read(f)

        self.s = read_string(f)
        if not read_bool(f):
            self.p = read_string(f)
            
        self.t = spatial.create_point(f)
        self.r = read_bool(f)
        if object_version >= 2:
            self.v = read_bool(f)
            self.z = read_double(f)
            self.q = read_double(f)
        if object_version >= 3:
            self.x = spatial.create_point(f)