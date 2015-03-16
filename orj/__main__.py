import argparse
import logging
import os.path
import sys

from .drawing import drawers
from .file import parse_orj_file

logger = logging.getLogger(__name__)

argparser = argparse.ArgumentParser(
    description="File conversion for ORJ floorplan files")
argparser.add_argument('filenames', metavar='filename', nargs='+',
                       help='.orj files to convert, starting with the bottom layer')
argparser.add_argument('-l', '--log-level',
                       dest='loglevel', action='store',
                       help="Python logging level")
argparser.add_argument('-x', '--width',
                       action='store', type=int, dest='width', default=1000,
                       help='Maximum image width in pixels')
argparser.add_argument('-y', '--height',
                       action='store', type=int, dest='height', default=1000,
                       help='Maximum image height in pixels')
argparser.add_argument('-m', '--margin',
                       action='store', type=int, dest='margin', default=1,
                       help='Image margin in pixels')
argparser.add_argument('-F', '--formats',
                       action='append', required=True,
                       choices=[d.format_name for d in drawers])

args = argparser.parse_args()
if args.loglevel:
    try:
        logging.basicConfig(level=getattr(logging, args.loglevel.upper()))
    except AttributeError:
        sys.stderr.write("{0} is not a valid log level".format(args.loglevel.upper()))
        sys.exit(1)

for filename in args.filenames:
    if not os.path.isfile(filename):
        sys.stderr.write("Couldn't find file: {0}\n".format(filename))
        sys.exit(1)

databases = []
for filename in args.filenames:
    logger.info("Reading %s", filename)
    with open(filename, 'rb') as f:
        database = parse_orj_file(f)
        databases.append(database)

base_filename, _ = os.path.splitext(args.filenames[0])

for drawer_cls in drawers:
    if drawer_cls.format_name not in args.formats:
        continue
    drawer = drawer_cls(databases, args.width, args.height, args.margin)
    result = drawer.draw()
    with open(base_filename + drawer.default_extension, 'wb') as f:
         logger.info("Writing %s", f.name)
         drawer.write(f, result)

