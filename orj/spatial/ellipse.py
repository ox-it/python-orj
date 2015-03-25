from math import sin, cos, pi, atan2, sqrt, tan, atan

from ..bounding_box import BoundingBox
from ..drawing import SVG

from .point import Point

class Ellipse(object):
    def __init__(self, center, major_axis_direction, ratio, start_angle, angle):
        self.center = center
        self.major_axis_direction = major_axis_direction
        self.x_axis_rotation = atan2(major_axis_direction.y,
                                     major_axis_direction.x)
        self.rx = sqrt(major_axis_direction.x ** 2 + major_axis_direction.y ** 2)
        self.ry = self.rx * ratio
        self.ratio = ratio
        self.start_angle = start_angle % (pi * 2)
        self.angle = angle
        self.end_angle = (start_angle + angle) % (pi * 2)

    def draw_cairo(self, coord_context, stroke_context):
        with coord_context as context:
            context.arc(self.center.x, self.center.y,
                        self.radius,
                        0, pi * 2)
        with stroke_context as context:
            context.stroke()

    def get_bounding_box(self):
        # See http://fridrich.blogspot.com/2011/06/bounding-box-of-svg-elliptical-arc.html
        # to get a better understanding of what's going on here.
        # The bounding box is that of up to six points: the two ends of the
        # segment, and any of the four extrema of the ellipse in x and y that
        # lie on the segment.
        ps = [self.point_at(self.start_angle),
              self.point_at(self.end_angle)]

        # These are the extrema in x and y for the whole ellipse (i.e. not
        # just the segment). If they are not on the segment then we don't use them.
        possibles = [   - atan2(self.ry * tan(self.x_axis_rotation), self.rx),
                     pi - atan2(self.ry * tan(self.x_axis_rotation), self.rx),
                          atan2(self.ry, tan(self.x_axis_rotation) * self.rx),
                     pi + atan2(self.ry, tan(self.x_axis_rotation) * self.rx)]
        for th in possibles:
            if self.start_angle < self.end_angle:
                if self.start_angle < th < self.end_angle:
                    ps.append(self.point_at(th))
            else:
                if self.start_angle < th or th < self.end_angle:
                    ps.append(self.point_at(th))
        xs, ys = [p.x for p in ps], [p.y for p in ps]
        return BoundingBox(min(xs), min(ys), max(xs), max(ys))

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
