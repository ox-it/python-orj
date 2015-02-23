import logging
from random import random
import sys
import cairocffi as cairo

#logging.basicConfig(level=logging.DEBUG)

from .file import parse_orj_file
from .db import Space

with open(sys.argv[1], 'rb') as f:
    database = parse_orj_file(f)

w, h = 1000, 1000

surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
context = cairo.Context(surface)
with context:
    context.set_source_rgb(1, 1, 1)  # White
    context.paint()
# Restore the default source which is black.

minx, miny, maxx, maxy = float('inf'), float('inf'), float('-inf'), float('-inf')
for obj in database.objects:
    try:
        get_bounding_box = obj.get_bounding_box
    except AttributeError:
        continue
    a, b, c, d = get_bounding_box()
    minx, miny = min(minx, a), min(miny, b)
    maxx, maxy = max(maxx, c), max(maxy, d)

largest_dimension = max(maxx - minx, maxy - miny)

class CoordContext(object):
    def __init__(self, context):
        self.context = context

    def __enter__(self):
        self.context.save()
        print h, largest_dimension
        self.context.translate(0, h)
        self.context.scale(h/largest_dimension, -h/largest_dimension)
        self.context.translate(-minx, -miny)
        return self.context

    def __exit__(self, exc_type, exc_value, traceback):
        self.context.restore()

class StrokeContext(object):
    def __init__(self, context):
        self.context = context

    def __enter__(self):
        self.context.save()
        #context.set_source_rgba(random()/2, random()/2, random()/2)
        return self.context

    def __exit__(self, exc_type, exc_value, traceback):
        self.context.restore()

coord_context = CoordContext(context)
stroke_context = StrokeContext(context)

def tx(x):
    return w * (x - minx) / (maxx - minx)
def ty(y):
    return h - h * (y - miny) / (maxy - miny)


for obj in database.objects:
    try:
        draw_cairo = obj.draw_cairo
    except AttributeError:
        continue
    draw_cairo(coord_context, stroke_context)
surface.write_to_png('example.png')

sys.exit(0)

