class BoundingBox(object):
    def __init__(self, minx, miny, maxx, maxy):
        self.minx, self.miny = minx, miny
        self.maxx, self.maxy = maxx, maxy
        self.width = maxx - minx
        self.height = maxy - miny

    @classmethod
    def zero(cls):
        return cls(float('inf'), float('inf'), float('-inf'), float('-inf'))

    def __or__(self, other):
        cls = type(self)
        return cls(min(self.minx, other.minx),
                   min(self.miny, other.miny),
                   max(self.maxx, other.maxx),
                   max(self.maxy, other.maxy))

    @classmethod
    def union(cls, bounding_boxes):
        result = cls.zero()
        for bounding_box in bounding_boxes:
            result |= bounding_box
        return result

