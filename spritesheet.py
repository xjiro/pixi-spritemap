import argparse
import glob
import json
import os
import pprint
import math

from PIL import Image

import algorithms


parser=argparse.ArgumentParser(description="Spritesheet Generator for PixiJS")

parser.add_argument('-o',
                    '--output',
                    help="Output Location/Name",
                    type=str,
                    default='output/untitled_spritesheet')

parser.add_argument('-v',
                    '--verbose',
                    help="Verbose Debug Output",
                    action="store_true",
                    default=False)
                    
parser.add_argument('-a',
                    '--algorithm',
                    default='rectpack',
                    const='rectpack',
                    nargs='?',
                    choices=['simple', 'shelf', 'guillotine', 'maximal_rectangle', 'skyline'],
                    help='Algorithm for sprite orientation and placement')

parser.add_argument('-i',
                    '--input',
                    dest='input',
                    nargs='+',
                    metavar='INPUT',
                    required=True)

opts=parser.parse_args()


def verbose(*s):
    if opts.verbose:
        print(*s)


verbose("OPTIONS:", opts)


# gather input files
sprites = set()
for f in opts.input:
    for name in glob.glob(f):
        sprites.add(name)
sprites = list(sprites)

# load each input file
sprites = [Image.open(f) for f in sprites]

verbose('SPRITES:',pprint.pformat([x.filename for x in sprites]))

img = algorithms.gpacker(sprites, algorithm=opts.algorithm)

img.save(opts.output+'.png', format='png')


# commonpath = os.path.commonpath(opts.output)
# os.makedirs(commonpath, exist_ok=True)

# with open(opts.output+'.json', 'w+') as f:
#     json.dump({'dongs': 1}, f)
