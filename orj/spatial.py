import collections
from .utils import *

Point3D = collections.namedtuple('Point3D', ['x', 'y', 'z'])

class Polygon3D(object):
    def __init__(self, a, b=None):
        self.a = a
        self.b = b

def read_point_3d(f):
    x, y, z = read_double(f), read_double(f), read_double(f)
    return Point3D(x, y, z)

def read_polygon_3d_with_bulges_and_holes(f):
    v1 = []
    v2 = []

    for i in range(read_int(f)):
        v1.append(read_point_3d(f))

    if read_bool(f): # not sure what these are
        for i in range(len(v1)):
            v2.append(read_double(f))
        polygon_3d = Polygon3D(v1, v2)
    else:
        polygon_3d = Polygon3D(v1)

    if read_bool(f): # has holes
        for i in range(read_int(f)):
            hole = read_polygon_3d_with_bulges(f)
            polygon_3d.add_hole(hole)


    return polygon_3d

