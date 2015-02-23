from ..utils import *
from .entity import Entity

class Line(Entity):
    def read(self, f, ht):
        object_version = read_int(f)
        if object_version > 1:
            raise AssertionError
        super(Line, self).read(f)
