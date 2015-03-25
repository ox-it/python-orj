import math

from ..bounding_box import BoundingBox
from ..drawing import SVG

class Polyline(object):
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
        op = self.ps[0]
        path = ['M {0.x:.4f} {0.y:.4f}'.format(op)]
        for p in self.ps:
            dp = p - op
            if dp.x != 0 and dp.y != 0:
                path.append('l {0.x:.4f} {0.y:.4f}'.format(dp))
            elif dp.x != 0:
                path.append('h {0.x:.4f}'.format(dp))
            elif dp.y != 0:
                path.append('v {0.y:.4f}'.format(dp))
            op = p
        return SVG.path(d=' '.join(path))
