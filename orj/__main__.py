import logging
from random import random
import sys
import cairocffi as cairo

#logging.basicConfig(level=logging.DEBUG)

from .database import Database
from .db import Space
from .header import Header


database = Database()

with open(sys.argv[1], 'rb') as f:
    database.read(f)

w, h = 500, 500

surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
context = cairo.Context(surface)
with context:
    context.set_source_rgb(1, 1, 1)  # White
    context.paint()
# Restore the default source which is black.

minx, miny, maxx, maxy = float('inf'), float('inf'), float('-inf'), float('-inf')
for obj in database.objects:
    if not isinstance(obj, Space):
        continue
    for p in obj.polygon_3d.a:
        minx, miny = min(minx, p.x), min(miny, p.y)
        maxx, maxy = max(maxx, p.x), max(maxy, p.y)

if (maxx - minx) > (maxy - miny):
    h /= (maxx - minx) / (maxy - miny)
else:
    w /= (maxx - minx) / (maxy - miny)

def tx(x):
    return w * (x - minx) / (maxx - minx)
def ty(y):
    return h - h * (y - miny) / (maxy - miny)


for obj in database.objects:
    if not isinstance(obj, Space):
        continue
    polygon = obj.polygon_3d
    context.move_to(tx(polygon.a[0].x), ty(polygon.a[0].y))
    for p in polygon.a[1:]:
        context.line_to(tx(p.x), ty(p.y))
    context.set_source_rgba(random()/2, random()/2, random()/2, 0.2)
#    context.fill()
#    context.set_source_rgba(0, 0, 0)
    context.stroke()
surface.write_to_png('example.png')

sys.exit(0)

