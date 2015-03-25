from .vector import Vector

class Point(object):
    __slots__ = ['x', 'y', 'z']

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __sub__(self, other):
        return Vector(self.x - other.x,
                      self.y - other.y,
                      self.z - other.z)