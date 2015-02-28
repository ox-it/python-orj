import contextlib
import logging
from random import random
import sys
import cairocffi as cairo

from lxml import etree

logging.basicConfig(level=logging.DEBUG)

from .drawing import CairoDrawer, SVGDrawer
from .file import parse_orj_file
from .db import Space

with open(sys.argv[1], 'rb') as f:
    database = parse_orj_file(f)

width, height = 500, 500
margin = 10

drawer = CairoDrawer(database, width, height, margin)
surface = drawer.draw()
surface.write_to_png('example.png')

drawer = SVGDrawer(database, width, height, margin)
svg = drawer.draw()
with open('example.svg', 'wb') as f:
    f.write(etree.tostring(svg))
