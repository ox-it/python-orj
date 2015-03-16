import collections
import math
from random import random, randint

from .bounding_box import BoundingBox
from .drawing import SVG
from .utils import *

Point3D = collections.namedtuple('Point3D', ['x', 'y', 'z'])

class Polyline3D(object):
    def __init__(self, ps):
        # If we get lots of points in a line, we can ignore the points on the
        # line. A point is on the line iff there's the same angle between it
        # and the two points before and after it.
        self.ps = ps[:1]
        s = 0
        try:
            p0, p1 = ps[:2]
        except ValueError:
            pass
        else:
            for p2 in ps[2:]:
                th0 = math.atan2(p1.x - p0.x, p1.y - p0.y)
                th1 = math.atan2(p2.x - p1.x, p2.y - p1.y)
                if abs(th0 - th1) < 0.001:
                    s += 1
                    p1 = p2
                else:
                    self.ps.append(p1)
                    p0, p1 = p1, p2
            self.ps.append(p1)

    def get_bounding_box(self):
        minx, miny, maxx, maxy = float('inf'), float('inf'), float('-inf'), float('-inf')
        for p in self.ps:
            minx, miny = min(minx, p.x), min(miny, p.y)
            maxx, maxy = max(maxx, p.x), max(maxy, p.y)
        return BoundingBox(minx, miny, maxx, maxy)

    def draw_cairo(self, coord_context, stroke_context):
        if not self.ps:
            return
        with coord_context as context:
            context.move_to(self.ps[0].x, self.ps[0].y)
            for p in self.ps[1:]:
                context.line_to(p.x, p.y)
        with stroke_context as context:
            context.stroke()

    def draw_svg(self):
        px, py = map('{0:.4f}'.format, [self.ps[0].x, self.ps[1].y])
        path = ['M {0} {1}'.format(px, py)]
        for p in self.ps:
            npx, npy = map('{0:.4f}'.format, [p.x, p.y])
            if px != npx and py != npy:
                path.append('L {0} {1}'.format(npx, npy))
            elif px != npx and py == npy:
                path.append('H {0}'.format(npx))
            elif px == npx and py != npy:
                path.append('V {0}'.format(npy))
            px, py = npx, npy

        return SVG.path(d=' '.join(path))

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
        return SVG.polygon(points=' '.join('{0.x} {0.y}'.format(p) for p in self.a))

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

    def draw_svg(self):
        return SVG.line(x1=str(self.p1.x),
                        y1=str(self.p1.y),
                        x2=str(self.p2.x),
                        y2=str(self.p2.y))

class Circle3D(object):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def draw_cairo(self, coord_context, stroke_context):
        with coord_context as context:
            context.arc(self.center.x, self.center.y,
                        self.radius,
                        0, math.pi * 2)
        with stroke_context as context:
            context.stroke()

    def get_bounding_box(self):
        return BoundingBox(self.center.x - self.radius,
                           self.center.x + self.radius,
                           self.center.y - self.radius,
                           self.center.y + self.radius)

    def draw_svg(self):
        return SVG.circle(r=str(self.radius),
                          cx=str(self.center.x),
                          cy=str(self.center.y))

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

    def draw_svg(self):
        th0, th1 = self.start_angle, self.start_angle + self.angle
        p0 = Point3D(self.center.x + math.cos(th0) * self.radius,
                     self.center.y + math.sin(th0) * self.radius,
                     self.center.z)
        p1 = Point3D(self.center.x + math.cos(th1) * self.radius,
                     self.center.y + math.sin(th1) * self.radius,
                     self.center.z)
        large_arc = '1' if self.angle > math.pi else '0'

        return SVG.path(d='M {0.x:.4f} {0.y:.4f} A {1:.4f} {1:.4f} 0 {2} 1 {3.x:.4f} {3.y:.4f} '.format(p0, self.radius, large_arc, p1))

def read_point_3d(f):
    x, y, z = read_point(f)
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
