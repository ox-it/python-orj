from ..utils import *

from .group import Group
from .layer import Layer

class LayerList(Group):
    def __init__(self):
        self.layers = []
        super(LayerList, self).__init__()

    def read(self, f, id_map):
        object_version = read_int(f)
        if object_version > 2:
            raise AssertionError(object_version)
        if object_version >= 2:
            j = read_int(f)
            if j > 0:
                b = read_buffer(f)
                for i in range(j):
                    object_buffer = read_buffer(b)
                    name = read_string(object_buffer)
                    if name == 'DbLayer':
                        layer = Layer()
                        layer.read(object_buffer, id_map)
                        self.layers.append(layer)
        elif object_version >= 1:
            for i in range(read_int(f)):
                object_type_name = read_string(f)
                if object_type_name == 'DbLayer':
                    layer = Layer()
                    layer.read(f, id_map)
                    self.layers.append(layer)

    def simplify(self):
        for layer in self:
            layer.simplify()

    def __iter__(self):
        return iter(self.layers)
    def __reversed__(self):
        return reversed(self.layers)
