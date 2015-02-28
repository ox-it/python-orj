from ..bounding_box import BoundingBox
from ..drawing import SVG
from ..utils import *

from .group import Group

class Layer(Group):
    def __init__(self):
        self.objects = []
        super(Layer, self).__init__()

    def read(self, f, id_map):
        object_version = read_int(f)
        if object_version > 1:
            raise AssertionError
        self.name = read_string(f)
        self.visible = read_bool(f)
        for i in range(read_int(f)):
            object_id = read_long(f)
            self.objects.append(id_map[object_id])

    def __iter__(self):
        return iter(self.objects)
    def __reversed__(self):
        return reversed(self.objects)

    def get_bounding_box(self):
        return BoundingBox.union(obj.get_bounding_box()
                                     for obj in self.objects)

    def draw_cairo(self, coord_context, stroke_context):
        for obj in reversed(self.objects):
            obj.draw_cairo(coord_context, stroke_context)

    def draw_svg(self, elem):
        g = SVG.g(**{'class': 'Layer'})
        for obj in reversed(self.objects):
            obj.draw_svg(g)
        elem.append(g)

