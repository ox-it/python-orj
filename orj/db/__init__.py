from .arc import *
from .attribute import *
from .database import *
from .graph import *
from .group import *
from .header import *
from .layer_list import *
from .line import *
from .object import *
from .polyline import *
from .space import *
from .symbol_def import *
from .symbol_ref import *
from .text import *

registry = {}
registry_by_object_type = {}
for name, value in globals().items():
    if isinstance(value, type) and issubclass(value, Object):
        registry['Db' + name] = value
        if hasattr(value, 'object_type'):
            registry_by_object_type[value.object_type] = value

