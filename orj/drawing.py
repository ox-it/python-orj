from __future__ import absolute_import

import math

try:
    import cairocffi as cairo
except ImportError:
    import cairo

from lxml.builder import ElementMaker
from lxml import etree

from .bounding_box import BoundingBox

SVG = ElementMaker(namespace='http://www.w3.org/2000/svg',
                   nsmap={None: 'http://www.w3.org/2000/svg'})

class ContextWrapper(object):
    def __init__(self, context, update_context):
        self.context = context
        self.update_context = update_context

    def __enter__(self):
        self.context.save()
        self.update_context(self.context)
        return self.context

    def __exit__(self, exc_type, exc_value, traceback):
        self.context.restore()

class Drawer(object):
    def __init__(self, databases, max_width, max_height, margin=10, pad=True):
        self.databases = databases
        self.max_width = max_width
        self.max_height = max_height
        self.pad = pad
        self.margin = margin

        self.bounding_box = BoundingBox.zero()
        for database in databases:
            self.bounding_box |= database.get_bounding_box()

        self.drawing_aspect_ratio = self.bounding_box.width / self.bounding_box.height
        if self.drawing_aspect_ratio > 1:
            self.width = self.max_width
            self.inner_width = self.width - 2 * self.margin
            self.inner_height = int(math.ceil(self.inner_width / self.drawing_aspect_ratio))
            self.height = self.inner_height + 2 * self.margin
        else:
            self.height = self.max_height
            self.inner_height = self.height - 2 * self.margin
            self.inner_width = int(math.ceil(self.inner_height * self.drawing_aspect_ratio))
            self.width = self.inner_width + 2 * self.margin

        self.scale = min(self.inner_width / self.bounding_box.width,
                         self.inner_height / self.bounding_box.height)

class PNGDrawer(Drawer):
    media_type = 'image/png'
    default_extension = '.png'
    format_name = 'png'

    def coordinate_transform(self, context):
        # Applied in reverse order
        context.translate(self.margin,
                          self.height - self.margin)
        context.scale(self.scale, -self.scale)
        context.translate(-self.bounding_box.minx,
                          -self.bounding_box.miny)

    def stroke_style(self, context):
        context.set_line_width(1.0)

    def draw(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                     self.width, self.height)
        context = cairo.Context(surface)
        coord_context = ContextWrapper(context, self.coordinate_transform)
        stroke_context = ContextWrapper(context, self.stroke_style)
        for database in self.databases:
            database.draw_cairo(coord_context, stroke_context)
        return surface

    def write(self, f, surface):
        surface.write_to_png(f)

class SVGDrawer(Drawer):
    media_type = 'image/svg+xml'
    default_extension = '.svg'
    format_name = 'svg'

    def draw(self):
        stroke_width = '{:f}px'.format(1.0 / self.scale)
        svg = SVG.svg(width=str(self.width), height=str(self.height))
        g = SVG.g(**{'transform': " ".join([
                         "translate({0}, {1})".format(self.margin, self.height - self.margin),
                         "scale({0}, {1})".format(self.scale, -self.scale),
                         "translate({0}, {1})".format(-self.bounding_box.minx, -self.bounding_box.miny)]),
                     'fill': 'none',
                     'stroke': 'black',
                     'stroke-width': stroke_width})

        for database in self.databases:
            g.extend(database.draw_svg())
        svg.append(g)
        return svg

    def write(self, f, svg):
        f.write(etree.tostring(svg))

drawers = (
    PNGDrawer,
    SVGDrawer,
)