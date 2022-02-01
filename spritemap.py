import argparse
import glob
import json
import os
import pprint

from PIL import Image

import algorithms


parser = argparse.ArgumentParser(description="Spritemap Generator for PixiJS")

parser.add_argument('-v',
                    '--verbose',
                    help="Verbose Debug Output",
                    action="store_true",
                    default=False)

parser.add_argument('-o',
                    '--output',
                    help="Output Location/Name",
                    type=str,
                    default=os.path.join('output', 'spritesheet'))

parser.add_argument('-i',
                    '--input',
                    dest='input',
                    nargs='+',
                    metavar='INPUT',
                    default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input', '*'))

opts = parser.parse_args()


def verbose(*s):
    if opts.verbose:
        print(*s)


verbose("OPTIONS:", opts)

# gather input files
sprites = set()

# opts.input is a single string (not a list) if <2 values provided
for f in (opts.input if type(opts.input) == list else [opts.input]):
    for name in glob.glob(f):
        sprites.add(name)
sprites = list(sprites)

verbose('INPUT:', pprint.pformat(sprites))

# load each input file
sprites = [Image.open(f) for f in sprites]

img, sizes, pos = algorithms.rpacker(sprites)

commonpath = os.path.commonpath([s.filename for s in sprites])
verbose("COMMONPATH:", commonpath)

sprites_index = {"frames": {os.path.relpath(s.filename, commonpath).replace(os.sep, '.'): {"frame": {"x": pos[i][0], "y": pos[i][1], "w": s.width, "h": s.height},
                                         "rotated": False,
                                         "trimmed": False,
                                         "spriteSourceSize": {"x": 0, "y": 0, "w": s.width, "h": s.height},
                                         "sourceSize": {"w": s.width, "h": s.height}} for i, s in enumerate(sprites)},
                 "meta": {"app": "https://github.com/xjiro/spritemap-json",
                          "version": "1.0",
                          "image": "diasteroids.png",
                          "format": "RGBA8888",
                          "size": {"w": 1600, "h": 1600},
                          "scale": "1",
                          }}

img.save(opts.output+'.png', format='png')

with open(opts.output+'.json', 'w+') as f:
    json.dump(sprites_index, f)
