from ..enums import ObjectType
from ..utils import *
from .. import spatial

from .entity import Entity

class Space(Entity):
    object_type = ObjectType.SPACE

    def read(self, f, ht):
        object_version = read_int(f)
        if object_version > 4:
            raise AssertionError
        super(Space, self).read(f)

        if object_version >= 4:
            self.geometry = spatial.create_polygon_with_bulges_and_holes(f)
        else:
            raise AssertionError

        self.centroid = spatial.create_point(f)

        # There's a bug (for (int m = 0; m > k; m++) {...}) in orviewer that means
        # this would never work if the returned int isn't zero
        for i in range(read_int(f)):
            raise AssertionError

        if object_version >= 2:
            read_bool(f) # not sure what this means

#        assert not f.read(1) # Make sure we've consumed the entire buffer

    def draw_svg(self):
        for elem in super(Space, self).draw_svg():
            elem.attrib['fill'] = '#' + ''.join('%02x' % c for c in self.color)
            elem.attrib['fill-opacity'] = '0.1'
            elem.attrib['stroke'] = 'none'
            if 'FMObjectType' in self.attributes:
                elem.attrib['class'] = self.attributes['FMObjectType'].value
            yield elem

