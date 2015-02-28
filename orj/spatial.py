import collections
from random import random, randint

from .bounding_box import BoundingBox
from .drawing import SVG
from .utils import *

Point3D = collections.namedtuple('Point3D', ['x', 'y', 'z'])

class Polyline3D(object):
    def __init__(self, ps):
        self.ps = ps

class Polygon3D(object):
    def __init__(self, a, b=None):
        self.holes = []
        self.a = a
        self.b = b

    def add_hole(self, hole):
        self.holes.append(hole)

    def draw_cairo(self, coord_context, stroke_context, is_hole=False):
        with coord_context as context:
            context.move_to(self.a[0].x, self.a[0].y)
            for p in self.a[1:]:
                context.line_to(p.x, p.y)
        with stroke_context as context:
            context.set_source_rgba(random(), random(), random()/2)
            context.fill()
        with coord_context as context:
            context.move_to(self.a[0].x, self.a[0].y)
            for p in self.a[1:]:
                context.line_to(p.x, p.y)
        with stroke_context as context:
            context.stroke()

#            if is_hole:
#                context.set_source_rgba(1, 0, 0, 1)
#            #context.fill()
#            context.stroke()

        for hole in self.holes:
            hole.draw_cairo(coord_context, stroke_context, is_hole=True)

    def draw_svg(self):
        return SVG.polygon(**{'stroke-width': '0px',
                              'fill': '#%06x' % randint(0, 256**3),
                              'points': ' '.join('{0.x} {0.y}'.format(p) for p in self.a),
                              'vector-effect': 'non-scaling-stroke'})

    def get_bounding_box(self):
        minx, miny, maxx, maxy = float('inf'), float('inf'), float('-inf'), float('-inf')
        for p in self.a:
            minx, miny = min(minx, p.x), min(miny, p.y)
            maxx, maxy = max(maxx, p.x), max(maxy, p.y)
        return BoundingBox(minx, miny, maxx, maxy)

class Line3D(object):
    def __init__(self, p1, p2):
        self.p1, self.p2 = p1, p2

    def draw_cairo(self, coord_context, stroke_context):
        with coord_context as context:
            context.move_to(self.p1.x, self.p1.y)
            context.line_to(self.p2.x, self.p2.y)
        with stroke_context as context:
            context.stroke()

    def get_bounding_box(self):
        return BoundingBox(min(self.p1.x, self.p2.x),
                           min(self.p1.y, self.p2.y),
                           max(self.p1.x, self.p2.x),
                           max(self.p1.y, self.p2.y))

class Arc3D(object):
    def __init__(self, center, radius, start_angle, angle):
        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.angle = angle

    def draw_cairo(self, coord_context, stroke_context):
        with coord_context as context:
            context.arc(self.center.x, self.center.y,
                        self.radius, 
                        self.start_angle,
                        self.start_angle + self.angle)
        with stroke_context as context:
            context.stroke()

    def get_bounding_box(self):
        return BoundingBox(self.center.x - self.radius,
                           self.center.x + self.radius,
                           self.center.y - self.radius,
                           self.center.y + self.radius)

def read_point_3d(f):
    x, y, z = read_double(f), read_double(f), read_double(f)
    return Point3D(x, y, z)

def read_polygon_3d_with_bulges(f):
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

    return polygon_3d

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

def read_polyline_3d(f):
    ps = []
    for i in range(read_int(f)):
        ps.append(read_point_3d(f))
    return Polyline3D(ps)

def read_transform_3d(f):
    pass
