import math
from PIL import Image

import rectpack

def rppacker(sprites):
    packer = rectpack.newPacker(mode=rectpack.PackingMode.Offline,
                                rotation=True)

    for s in sprites:
        packer.add_rect(s.width, s.height, s.filename)

    width = sum([s.width for s in sprites])
    height = sum([s.height for s in sprites])
    side = math.ceil(math.sqrt(1.2 * sum([s.width * s.height for s in sprites])).real)

    packer.add_bin(side, side)

    packer.pack()

    all_rects = packer.rect_list()

    img = Image.new(mode="RGBA", size=(width, height))

    print(all_rects)

    for rect in all_rects:
        b, x, y, w, h, rid = rect
        sprite = [s for s in sprites if s.filename == rid][0]

        if w != h and w == s.height:
            sprite.rotate(90)

        # print(b, x, y, w, h, rid)
        img.paste(sprite, (x, y,))

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
