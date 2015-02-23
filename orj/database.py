import StringIO
from .db import Graph, Group, LayerList, Object, DatabaseHeader
from .utils import *
from .enums import ObjectType
from .object_registry import registry_by_id

class Database(Object):
    def __init__(self):
        self.header = DatabaseHeader()
        self.graph = Graph()
        self.symbol_def_list = Group()
        self.objects = []
        self.id_map = {}
        self.layer_list = LayerList()

    def read(self, f):
        object_version = self.read_object_version(f)
        if object_version != 3:
            raise NotImplementedError

        self.header.read(read_buffer(f))

        ht1 = {}
        self.graph.read(read_buffer(f), ht1)

        ht2 = {}
        self.symbol_def_list.read(read_buffer(f), ht2)

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
                    cls = registry_by_id[object_type]
                    obj = cls()
                    obj.read(object_buffer, ht1)
                    self.objects.append(obj)
                    self.id_map[obj.object_id] = obj

        layer_list_buffer = read_buffer(f)
        if layer_list_buffer.len:
            self.layer_list.read(layer_list_buffer, self.id_map)

