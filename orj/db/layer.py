import collections

from ..bounding_box import BoundingBox
from ..drawing import SVG
from .. import spatial
from ..utils import *

from .group import Group
from .line import Line
from .polyline import Polyline

class Layer(Group):
    def __init__(self):
        self.objects = []
        super(Layer, self).__init__()

    def read(self, f, id_map):
        object_version = read_int(f)
        if object_version > 1:
            raise AssertionError
        self.name = read_string(f)
        self.visible = read_bool(f)
        for i in range(read_int(f)):
            object_id = read_long(f)
            try:
                self.objects.append(id_map[object_id])
            except KeyError:
                pass # The original implementation doesn't mind missing objects either

    def __iter__(self):
        return iter(self.objects)
    def __reversed__(self):
        return reversed(self.objects)

    def get_bounding_box(self):
        return BoundingBox.union(obj.get_bounding_box()
                                     for obj in self.objects)

    def draw_cairo(self, coord_context, stroke_context):
        for obj in reversed(self.objects):
            obj.draw_cairo(coord_context, stroke_context)

    def draw_svg(self):
        g = SVG.g(**{'class': 'Layer'})
        for i, obj in enumerate(reversed(self.objects)):
            if i % 10 != 9:
                continue
            g.extend(obj.draw_svg())
        yield g

    def simplify(self):
        points = collections.defaultdict(list)
        for obj in self.objects:
            if isinstance(obj, Line):
                geom = obj.geometry
                points[geom.p1].append(([geom.p2], obj))
                points[geom.p2].append(([geom.p1], obj))
            elif isinstance(obj, Polyline):
                geom = obj.geometry
                points[geom.ps[0]].append(([geom.ps[1:]], obj))
                points[geom.ps[-1]].append((reversed([geom.ps[:-1]]), obj))
        
        print len(points)
        filtered_points = {}
        while points:
            p, outward = points.popitem()
            if len(outward) > 1:
                filtered_points[p] = outward
        points = filtered_points
        print len(points)
        
        to_remove, polylines = set(), []
        while points:
            p, outward = points.popitem()
            ps, obj = outward.pop()
            ps.insert(0, p)
            if outward:
                points[p] = outward
            if ps[-1] not in points:
                continue
            to_remove.add(obj)
            while ps[-1] in points:
                outward = points[ps[-1]]
                new_ps, new_obj = outward.pop()
                if not outward:
                    del points[ps[-1]]
                if new_obj in to_remove:
                    continue
                to_remove.add(new_obj)
                ps.extend(new_ps)
            polylines.append(ps)
        self.objects = [o for o in self.objects if o not in to_remove]
        for ps in polylines:
            print ps
            obj = Polyline()
            obj.geometry = spatial.Polyline(ps)
            self.objects.append(obj)