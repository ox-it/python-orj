from ..utils import *

from .arc import Arc
from .circle import Circle
from .ellipse import Ellipse
from .line import Line
from .point import Point
from .polygon import Polygon
from .polyline import Polyline
from .vector import Vector

def create_point(f):
    x, y, z = read_point(f)
    return Point(x, y, z)

def create_vector(f):
    x, y, z = read_point(f)
    return Vector(x, y, z)

def create_circle(f):
    return Circle(create_point(f), read_double(f))

def create_ellipse(f):
    return Ellipse(create_point(f),
                   create_vector(f),
                   read_double(f),
                   read_double(f),
                   read_double(f))

def create_arc(f):
    return Arc(center=create_point(f),
               radius=read_double(f),
               start_angle=read_double(f),
               angle=read_double(f))

def create_line(f):
    return Line(create_point(f),
                create_point(f))

def create_polygon_with_bulges(f):
    v1 = []
    v2 = []

    for i in range(read_int(f)):
        v1.append(create_point(f))

    if read_bool(f): # not sure what these are
        for i in range(len(v1)):
            v2.append(read_double(f))
        polygon_3d = Polygon(v1, v2)
    else:
        polygon_3d = Polygon(v1)

    return polygon_3d

def create_polygon_with_bulges_and_holes(f):
    v1 = []
    v2 = []

    for i in range(read_int(f)):
        v1.append(create_point(f))

    if read_bool(f): # not sure what these are
        for i in range(len(v1)):
            v2.append(read_double(f))
        polygon_3d = Polygon(v1, v2)
    else:
        polygon_3d = Polygon(v1)

    if read_bool(f): # has holes
        for i in range(read_int(f)):
            hole = create_polygon_with_bulges(f)
            polygon_3d.add_hole(hole)


    return polygon_3d

def create_polyline(f):
    ps = []
    for i in range(read_int(f)):
        ps.append(create_point(f))
    return Polyline(ps)

def create_transform(f):
    pass
