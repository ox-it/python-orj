class ORJException(Exception):
    pass

class ParseError(ORJException):
    pass

class UnsupportedObjectVersion(ParseError):
    pass