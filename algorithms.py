import math
from PIL import Image

import greedypacker

def gpacker(sprites, algorithm='maximal_rectangle'):

    width = sum([s.width for s in sprites])
    height = sum([s.height for s in sprites])

    # side = math.ceil(math.sqrt(1.2 * sum([s.width * s.height for s in sprites])).real)

    heuristics = {'shelf': 'best_area_fit',
                  'guillotine': 'best_area',
                  'maximal_rectangle': 'best_longside',
                  'skyline': 'best_fit'}


    packer = greedypacker.BinManager(width, height, pack_algo=algorithm, heuristic=heuristics.get(algorithm), wastemap=False, rotation=True)

    sprite_items = []
    for s in sprites:
        item = greedypacker.Item(s.width, s.height)
        item.id = s.filename
        sprite_items.append(item)

    packer.add_items(*sprite_items)

    packer.execute()

    img = Image.new(mode="RGBA", size=(width, height))

    for i in packer.bins[0].items:
        sprite = [s for s in sprites if s.filename == i.id][0]

        if i.width != i.height and i.width != sprite.width:
            sprite = sprite.rotate(90, expand=True)

        img.paste(sprite, (i.x, i.y,))

    img = img.crop(img.getbbox())

    # x, y = 0, 0
    # for row in grid:
    #     for subimg in row:
    #         img.paste(subimg, (x, y,))
    #         x += subimg.width

    #     y += max([subimg.height for subimg in row])
    #     x = 0
    
    return img


def simple(sprites):
    num = len(sprites)
    num_w = math.ceil(sqrt(num).real)

    sprites = sorted(sprites, key=lambda x: x.width)

    paired_sprites = []
    while sprites:
        paired_sprites.append(sprites.pop(0))
        if sprites:
            paired_sprites.append(sprites.pop())

    grid = [paired_sprites[i*num_w:(i+1)*num_w] for i in range(num_w)]

    max_w = max([sum([x.width for x in r]) for r in grid])
    max_h = sum([max([x.height for x in r]) for r in grid])

    img = Image.new(mode="RGBA", size=(max_w, max_h))

    x, y = 0, 0
    for row in grid:
        for subimg in row:
            img.paste(subimg, (x, y,))
            x += subimg.width

        y += max([subimg.height for subimg in row])
        x = 0
    
    return img
