from ..utils import *

from .object import Object

class Entity(Object):
    parent_object_id = None
    geometry = None

    def read(self, f):
        object_version = read_int(f)
        if object_version > 4:
            raise NotImplementedError
        super(Entity, self).read(f)

        self.color = read_color(f)
        
        if object_version >= 2:
            self.fill = read_bool(f)
            if read_bool(f):
                self.fill_color = read_color(f)
            else:
                self.fill_color = None
        if object_version >= 3:
            if read_bool(f):
                self.parent_object_id = read_long(f)
        if object_version >= 4:
            self.line_type = read_short(f)

    def draw_cairo(self, coord_context, stroke_context):
        self.geometry.draw_cairo(coord_context, stroke_context)

    def get_bounding_box(self):
        return self.geometry.get_bounding_box()

