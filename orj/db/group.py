from ..enums import ObjectType
from ..utils import *
from .entity import Entity

class Group(Entity):
    def __init__(self):
        self.objects = []
        super(Group, self).__init__()

    def read(self, f, ht):
        object_version = read_int(f)
        if object_version != 3:
            raise NotImplementedError
        super(Group, self).read(f)
        k = read_int(f)
        if k > 0:
            b = read_buffer(f)

            for m in range(k):
                entity_buffer = read_buffer(b)
                if entity_buffer.len:
                    try:
                        x = read_byte(entity_buffer)
                        object_type = ObjectType(x)
                    except ValueError:
                        name = read_string(entity_buffer)
                        print ("XX", x, name)
                        raise AssertionError
                    else:
                        from . import registry_by_object_type
                        cls = registry_by_object_type[object_type]
                        obj = cls()
                        obj.read(entity_buffer, ht)
                        self.objects.append(obj)

