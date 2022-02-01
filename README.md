# pixi-spritemap

Utility to merge sprites and generate the spritemap.json for [PixiJS](https://pixijs.com/).


## Usage
`spritemap.py [-h] [-v] [-o OUTPUT] [-i INPUT [INPUT ...]]`

----
By default, spritemap will combine `input/*` and create `spritesheet.png`, `spritesheet.json` in `output/`:

```bash
> python spritemap.py
Packed Density:  91 %
```
Common paths will be removed from the frame name. `input/ship.png` will be `ship.png`

----

You can also feed spritemap multiple input directories, and the output frames will be prefixed with uncommon path components:

```bash
> python spritemap.py -i redteam/* blueteam/*
Packed Density:  97 %
```
So `redteam/ship.png` and `blueteam/ship.png` will not conflict and will be named `redteam.ship.png` and `blueteam.ship.png`

## License
[MIT](https://choosealicense.com/licenses/mit/)
