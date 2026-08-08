import pygame as pg

mapping = {
    (255, 0, 0): "texture@pykinst::red",
    (255, 255, 0): "texture@pykinst::yellow",
    (255, 0, 255): "texture@pykinst::magenta",
    (0, 255, 255): "texture@pykinst::sky",
    (0, 255, 0): "texture@pykinst::green",
    (0, 0, 255): "texture@pykinst::blue",
    (255, 255, 255): "texture@pykinst::cloud"
}


def map_create(image:pg.Surface, mapping:dict) -> list[list]:
    img = image.copy()

    map_width, map_height = img.get_size()
    map = []

    for src, tile in mapping.items():
        for x in range(map_width):
            for y in range(map_height):
                color = img.get_at((x, y))[:3]
                if color == src:
                    while len(map) <= y:
                        map.append([])
                    while len(map[y]) <= x:
                        map[y].append(None)
                    map[y][x] = tile
    return map