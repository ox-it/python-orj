from ..utils import *
from .entity import Entity

class Graph(Entity):
    def read(self, f, ht):
        object_version = read_int(f)
        if object_version > 1:
            raise NotImplementedError
        super(Graph, self).read(f)

