import StringIO

from ..bounding_box import BoundingBox
from ..utils import *
from ..enums import ObjectType

from .graph import Graph
from .group import Group
from .layer_list import LayerList
from .object import Object
from .header import DatabaseHeader

class Database(Object):
    def __init__(self):
        self.header = DatabaseHeader()
        self.graph = Graph()
        self.symbol_defs = Group()
        self.objects = []
        self.id_map = {}
        self.layers = LayerList()
        self.symbol_def_data = {}
        super(Database, self).__init__()

    def read(self, f):
        object_version = self.read_object_version(f)
        if object_version != 3:
            raise NotImplementedError

        self.header.read(read_buffer(f))

        ht1 = {}
        self.graph.read(read_buffer(f), ht1)


        self.symbol_defs.read(read_buffer(f),
                              self.symbol_def_data)

        i1 = read_int(f)
        if i1 > 0:
            i9 = read_buffer(f)
            for i in range(i1):
                object_buffer = read_buffer(i9)
                try:
                    object_type = ObjectType(read_byte(object_buffer))
                except ValueError:
                    raise AssertionError
                else:
                    from . import registry_by_object_type
                    cls = registry_by_object_type[object_type]
                    obj = cls()
                    obj.read(object_buffer, ht1)
                    self.objects.append(obj)
                    self.id_map[obj.object_id] = obj

        layer_list_buffer = read_buffer(f)
        if layer_list_buffer.len:
            self.layers.read(layer_list_buffer, self.id_map)
            self.layers.simplify()

    def get_bounding_box(self):
        return BoundingBox.union(obj.get_bounding_box()
                                     for obj in self.objects)

    def draw_cairo(self, coord_context, stroke_context):
        if self.layers:
            for layer in reversed(self.layers):
                layer.draw_cairo(coord_context, stroke_context)
        else:
            for obj in reversed(self.objects):
                obj.draw_cairo(coord_context, stroke_context)

    def draw_svg(self):
        if self.layers:
            for layer in reversed(self.layers):
                for elem in layer.draw_svg():
                    yield elem
        else:
            for obj in reversed(self.objects):
                for elem in obj.draw_svg():
                    yield elem

