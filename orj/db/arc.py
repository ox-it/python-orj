from ..utils import *
from .entity import Entity

class Arc(Entity):
    def read(self, f, ht):
        object_version = read_int(f)
        if object_version > 1:
            raise AssertionError
        super(Arc, self).read(f)
