import functools
import inspect
import logging
import StringIO
import struct

logger = logging.getLogger(__name__)

def _log(func):
    @functools.wraps(func)
    def wrapped(f):
        value = func(f)
        frame = inspect.stack()[1]
        logger.debug("%s: %r", frame[4][frame[5]].strip(), value)
        return value
    return wrapped

@_log
def read_int(f):
    return struct.unpack('>i', f.read(4))[0]

@_log
def read_byte(f):
    return struct.unpack('b', f.read(1))[0]

@_log
def read_string(f):
    # A string is preceded by its length in characters. Each character is
    # two bytes (UTF-16, big-endian)
    return f.read(struct.unpack('>i', f.read(4))[0] * 2).decode('utf-16-be')

@_log
def read_bool(f):
    return struct.unpack('?', f.read(1))[0]

@_log
def read_short(f):
    return struct.unpack('>h', f.read(2))[0]

@_log
def read_long(f):
    return struct.unpack('>q', f.read(8))[0]

@_log
def read_color(f):
    return struct.unpack('>iii', f.read(12))

@_log
def read_double(f):
    return struct.unpack('>d', f.read(8))[0]

@_log
def read_buffer(f):
    size = read_int(f)
    return StringIO.StringIO(f.read(size))
