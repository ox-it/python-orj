from ..utils import *
from .. import spatial
from .entity import Entity

class Space(Entity):
    def read(self, f, ht):
        object_version = read_int(f)
        if object_version > 4:
            raise AssertionError
        super(Space, self).read(f)

        if object_version >= 4:
            self.polygon_3d = spatial.read_polygon_3d_with_bulges_and_holes(f)
        else:
            raise AssertionError

        self.point = spatial.read_point_3d(f)

        # There's a bug (for (int m = 0; m > k; m++) {...}) in orviewer that means
        # this would never work if the returned int isn't zero
        for i in range(read_int(f)):
            raise AssertionError

        if object_version >= 2:
            read_bool(f) # not sure what this means

        assert not f.read(1) # Make sure we've consumed the entire buffer

