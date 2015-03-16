from ..bounding_box import BoundingBox
from ..drawing import SVG

class Line(object):
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
