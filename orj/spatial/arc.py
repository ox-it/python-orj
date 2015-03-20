import math

from ..bounding_box import BoundingBox
from ..drawing import SVG

from .ellipse import Ellipse
from .point import Point
from .vector import Vector

class Arc(Ellipse):
    def __init__(self, center, radius, start_angle, angle):
        super(Arc, self).__init__(center,
                                  Vector(radius, 0, 0), 1,
                                  start_angle, angle)
