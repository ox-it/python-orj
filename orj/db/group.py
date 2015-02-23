from ..utils import *
from .entity import Entity

class Group(Entity):
    def read(self, f, ht):
        object_version = read_int(f)
        if object_version != 3:
            raise NotImplementedError
        super(Group, self).read(f)

        count = read_int(f)
