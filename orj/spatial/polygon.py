from random import random

from ..bounding_box import BoundingBox
from ..drawing import SVG

class Polygon(object):
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
