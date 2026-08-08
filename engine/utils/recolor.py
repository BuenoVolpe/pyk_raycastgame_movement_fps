import pygame as pg
from engine.configs.configs import configs

def recolor (image:pg.Surface, color_map:dict, use_colorkey_on_color_map:bool=False) -> pg.Surface:
    img = image.copy()
    px = pg.PixelArray(img)

    engine = configs.engine

    for src, dst in color_map.items():
        if not use_colorkey_on_color_map:
            if list(src) in [engine.get("color_key1", [255, 0, 255]), engine.get("color_key2", [175, 0, 175])]:
                # px.replace(src, (0,0,0,0))
                continue
        px.replace(src, dst[:4])

    del px
    return img

def darken_color(color:list, factor:float=0.7) -> tuple:
    r, g, b = color
    r = min(max(int(r * factor), 0), 255)
    g = min(max(int(g * factor), 0), 255)
    b = min(max(int(b * factor), 0), 255)
    return (r, g, b)

def apply_multi_colorkey(surface, colors):
    surface = surface.convert_alpha()

    colors = {tuple(c) for c in colors}

    w, h = surface.get_size()

    for x in range(w):
        for y in range(h):
            if surface.get_at((x, y))[:3] in colors:
                surface.set_at((x, y), (0, 0, 0, 0))

    return surface


