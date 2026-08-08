from numba import njit
import math
import numpy as np
from engine.configs.configs import configs


sprite_tex_sum = np.int32(0)#settings.get("raycast_sprite_tex_sum", 0))
# settings.get("color_key1", [255, 0, 255])
# settings.get("color_key2", [175, 0, 175])
COLORKEY_1 = np.int32(0xFF00FF)
COLORKEY_2 = np.int32(0xAF00AF)

@njit(fastmath=True)
def render_sprites(
    posX, posY,
    dirX, dirY,
    planeX, planeY,
    sprites,
    textures,
    buffer,
    zbuffer,
    max_transformY=20,
    TEX_W = 32,
    TEX_H = 32
):
    tex_sum = sprite_tex_sum
    h, w = buffer.shape
    num_sprites = sprites.shape[0]

    # ordenar manualmente (selection sort simples)
    order = list(range(num_sprites))
    dist = [0.0] * num_sprites

    for i in range(num_sprites):
        dx = posX - sprites[i, 0]
        dy = posY - sprites[i, 1]
        dist[i] = dx*dx + dy*dy

    for i in range(num_sprites):
        for j in range(i+1, num_sprites):
            if dist[i] < dist[j]:
                dist[i], dist[j] = dist[j], dist[i]
                order[i], order[j] = order[j], order[i]

    for i in range(num_sprites):
        sprite = sprites[order[i]]

        spriteX = sprite[0] - posX
        spriteY = sprite[1] - posY

        invDet = 1.0 / (planeX*dirY - dirX*planeY)

        transformX = invDet * (dirY*spriteX - dirX*spriteY)
        transformY = invDet * (-planeY*spriteX + planeX*spriteY)

        if transformY <= 0 or transformY > max_transformY:
            continue

        spriteScreenX = int((w / 2) * (1 + transformX / transformY))

        scale = sprite[3]
        spriteHeight = abs(int(h / transformY * scale))
        offsetZ = sprite[4]
        screen_offset = int(offsetZ / transformY * h)

        drawStartY = max(-spriteHeight // 2 + h // 2 - screen_offset, 0)
        drawEndY = min(spriteHeight // 2 + h // 2 - screen_offset, h - 1)

        spriteWidth = spriteHeight
        drawStartX = max(-spriteWidth // 2 + spriteScreenX, 0)
        drawEndX = min(spriteWidth // 2 + spriteScreenX, w - 1)

        tex_id = int(sprite[2]) + tex_sum

        for stripe in range(drawStartX, drawEndX):
            if 0 <= stripe < w and transformY < zbuffer[stripe]:

                texX = int((stripe - (-spriteWidth//2 + spriteScreenX)) * TEX_W / spriteWidth)

                for y in range(drawStartY, drawEndY):
                    d = (y + screen_offset) * 256 - h * 128 + spriteHeight * 128
                    texY = ((d * TEX_H) // spriteHeight) // 256

                    if 0 <= texY < TEX_H:
                        color = textures[tex_id, texY, texX & (TEX_W-1)]

                        if color != COLORKEY_1 and color != COLORKEY_2:
                            buffer[y, stripe] = color

                    
