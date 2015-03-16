import math

from ..bounding_box import BoundingBox
from ..drawing import SVG

from .point import Point

class Arc(object):
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

    arc_svg_path = 'M {0.x:.4f} {0.y:.4f} A {1:.4f} {1:.4f} 0 {2} 1 {3.x:.4f} {3.y:.4f}'

    def draw_svg(self):
        th0, th1 = self.start_angle, self.start_angle + self.angle
        p0 = Point(self.center.x + math.cos(th0) * self.radius,
                   self.center.y + math.sin(th0) * self.radius,
                   self.center.z)
        p1 = Point(self.center.x + math.cos(th1) * self.radius,
                   self.center.y + math.sin(th1) * self.radius,
                   self.center.z)
        large_arc = '1' if self.angle > math.pi else '0'

        return SVG.path(d=self.arc_svg_path.format(p0, self.radius, large_arc, p1))
