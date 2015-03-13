from ..enums import ObjectType, TextAlignment
from .. import spatial
from ..utils import *

from .entity import Entity

class Text(Entity):
    object_type = ObjectType.TEXT

    def read(self, f, ht):
        object_version = read_int(f)
        if object_version > 5:
            raise AssertionError
        super(Text, self).read(f)
        self.text = read_string(f).encode('utf-8')
        self.position = spatial.read_point_3d(f)
        if object_version >= 2:
            self.font_size = read_int(f)
            self.is_multiline = read_bool(f)
            if self.is_multiline:
                self.text_list = []
                for i in range(read_int(f)):
                    self.text_list.append(read_string(f))
        if object_version >= 3:
            self.font_height = read_double(f)
        if object_version >= 4:
            self.angle = read_double(f)
        if object_version >= 5:
            self.alignment = TextAlignment(read_int(f))


            
        self.geometry = spatial.read_polyline_3d(f)

    def draw_svg(self):
        return ()
