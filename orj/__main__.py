import argparse
import logging

from lxml import etree

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


args = argparser.parse_args()
if args.loglevel:
    try:
        logging.basicConfig(level=getattr(logging, args.loglevel.upper()))
    except AttributeError:
        raise ValueError("{0} is not a valid log level".format(args.loglevel.upper()))

from .drawing import CairoDrawer, SVGDrawer
from .file import parse_orj_file

databases = []
for filename in args.filenames:
    with open(filename, 'rb') as f:
        database = parse_orj_file(f)
        databases.append(database)

drawer = CairoDrawer(databases, args.width, args.height, args.margin)
surface = drawer.draw()
surface.write_to_png('example.png')

drawer = SVGDrawer(databases, args.width, args.height, args.margin)
svg = drawer.draw()
with open('example.svg', 'wb') as f:
    f.write(etree.tostring(svg))
