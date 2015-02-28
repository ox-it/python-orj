from __future__ import absolute_import

try:
    import cairocffi as cairo
except ImportError:
    import cairo

from lxml.builder import ElementMaker

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
    def __init__(self, database, width, height, margin=10, pad=True):
        self.database = database
        self.width = width
        self.height = height
        self.pad = pad
        self.margin = margin
        self.inner_width = width - 2 * margin
        self.inner_height = height - 2 * margin

        self.bounding_box = self.database.get_bounding_box()
        self.canvas_aspect_ratio = self.inner_width / self.inner_height
        self.drawing_aspect_ratio = self.bounding_box.width / self.bounding_box.height

        self.scale = min(self.inner_width / self.bounding_box.width,
                         self.inner_height / self.bounding_box.height)

class CairoDrawer(Drawer):
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

        self.database.draw_cairo(coord_context, stroke_context)

class SVGDrawer(Drawer):
    def draw(self):
        svg = SVG.svg(width=str(self.width), height=str(self.height))
        g = SVG.g(transform=" ".join(([
            "translate({0}, {1})".format(self.margin, self.height - self.margin),
            "scale({0}, -{0})".format(self.scale),
            "translate(-{0.minx}, -{0.miny})".format(self.bounding_box),
        ])))
        self.database.draw_svg(g)
        svg.append(g)
        return svg
