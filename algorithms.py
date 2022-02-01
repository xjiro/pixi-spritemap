import math
from PIL import Image

import rpack

def rpacker(sprites):

    sizes = [(s.width, s.height,) for s in sprites]
    
    pos = rpack.pack(sizes)

    print("Packed Density: ", int(rpack.packing_density(sizes, pos)*100), '%')

    img = Image.new(mode="RGBA", size=rpack.bbox_size(sizes, pos))

    for i, s in enumerate(sprites):
        # if i.width != i.height and i.width != sprite.width:
        #     sprite = sprite.rotate(90, expand=True)
        img.paste(s, (pos[i][0], pos[i][1],))

    img = img.crop(img.getbbox())

    return img, sizes, pos


def simple(sprites):
    num = len(sprites)
    num_w = math.ceil(math.sqrt(num).real)

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
