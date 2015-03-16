import math

from ..bounding_box import BoundingBox
from ..drawing import SVG

class Circle(object):
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
