from math import sin, cos, pi, atan2, sqrt

from ..bounding_box import BoundingBox
from ..drawing import SVG

from .point import Point

class Ellipse(object):
    def __init__(self, center, major_axis_direction, ratio, start_angle, angle):
        self.center = center
        self.major_axis_direction = major_axis_direction
        self.x_axis_rotation = atan2(major_axis_direction.x,
                                     major_axis_direction.y)
        self.rx = sqrt(major_axis_direction.x ** 2 + major_axis_direction.y ** 2)
        self.ry = self.rx * ratio
        self.ratio = ratio
        self.start_angle = start_angle
        self.angle = angle
        self.end_angle = start_angle + angle

    def draw_cairo(self, coord_context, stroke_context):
        with coord_context as context:
            context.arc(self.center.x, self.center.y,
                        self.radius,
                        0, pi * 2)
        with stroke_context as context:
            context.stroke()

    def get_bounding_box(self):
        radius = max(self.rx, self.ry)
        return BoundingBox(self.center.x - radius,
                           self.center.x + radius,
                           self.center.y - radius,
                           self.center.y + radius)

    arc_svg_path = 'M {0.x:.4f} {0.y:.4f} A {1:.4f} {2:.4f} {3:.4f} {4} 1 {5.x:.4f} {5.y:.4f}'

    def point_at(self, theta):
        return Point(self.center.x + self.rx * cos(theta) * cos(self.x_axis_rotation)
                                   - self.ry * sin(theta) * sin(self.x_axis_rotation),
                     self.center.y + self.rx * cos(theta) * sin(self.x_axis_rotation)
                                   + self.ry * sin(theta) * cos(self.x_axis_rotation),
                     self.center.z)

    def draw_svg(self):
        p0 = self.point_at(self.start_angle)
        p1 = self.point_at(self.end_angle)
        large_arc = '1' if self.angle > pi else '0'

        return SVG.path(d=self.arc_svg_path.format(p0,
                                                   self.rx, self.ry,
                                                   self.x_axis_rotation,
                                                   large_arc, p1))
