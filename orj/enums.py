import enum

class Units(enum.Enum):
    MILLIMETER = 1
    CENTIMETER = 2
    DECIMETER = 3
    METER = 4
    INCH = 5
    FOOT = 6

class AttributeType(enum.Enum):
    STRING = 72
    DOUBLE = 73
    NGDATA = 74
    MATH = 75

class ObjectType(enum.Enum):
    LINE = 31
    ARC = 32
    CIRCLE = 33
    POLYGON = 34
    POLYLINE = 35
    TEXT = 36
    IMAGE = 37
    ELLIPSE = 38
    SPACE = 51
    WALL = 52
    OPENING = 53
    WINDOW = 54
    DOOR = 55
    SYMBOL_DEF = 56
    SYMBOL_REF = 57
    RED_LINE = 58
    LEGEND = 59

class TextAlignment(enum.Enum):
    LEFT = 0
