import zipfile

from .db import Database

def parse_orj_file(f):
    database = Database()
    database.read(f)
    return database

    orj_zipfile = zipfile.ZipFile(f)
    name = orj_zipfile.namelist()[0]
    database = Database()
    database.read(orj_zipfile.open(name))
    return database
