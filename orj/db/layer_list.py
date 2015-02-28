from ..utils import *

from .group import Group
from .layer import Layer

class LayerList(Group):
    def __init__(self):
        self.layers = []
        super(LayerList, self).__init__()

    def read(self, f, id_map):
        object_version = read_int(f)
        if object_version > 1:
            raise AssertionError
        for i in range(read_int(f)):
            object_type_name = read_string(f)
            if object_type_name == 'DbLayer':
                layer = Layer()
                layer.read(f, id_map)
                self.layers.append(layer)

    def __iter__(self):
        return iter(self.layers)
    def __reversed__(self):
        return reversed(self.layers)
