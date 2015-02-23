from .object import Object
from . import db
from .enums import ObjectType

registry = {}

for name in dir(db):
    if isinstance(getattr(db, name), Object):
        registry['Db' + name] = getattr(db, name)

registry_by_id = {
    ObjectType.SPACE: db.Space,
    ObjectType.LINE: db.Line,
    ObjectType.ARC: db.Arc,
}
