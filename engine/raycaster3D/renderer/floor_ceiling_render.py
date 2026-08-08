from numba import njit
import numpy as np
from engine.configs.configs import configs

settings_floor_tex_sum = 0#configs.get("raycast_floor_tex_sum", 0)
settings_ceil_tex_sum = 0#configs.get("raycast_ceil_tex_sum", 0)

@njit(fastmath=True)
def render_floor_ceiling(
    posX, posY, dirX, dirY, planeX, planeY,
    textures,
    buffer_out,
    ZBuffer,
    floorMap, ceilMap,
    floorDefaultTex1=1, floorDefaultTex2=1, ceilDefaultTex=2,
    TEX_W=32, TEX_H=32
):
    floor_tex_sum = settings_floor_tex_sum
    ceil_tex_sum = settings_ceil_tex_sum
    
    h, w = buffer_out.shape
    num_textures = textures.shape[0]
    floor_map_h, floor_map_w = floorMap.shape
    ceil_map_h, ceil_map_w = ceilMap.shape

    # direção dos raios para os cantos da tela
    rayDirX0 = dirX - planeX
    rayDirY0 = dirY - planeY
    rayDirX1 = dirX + planeX
    rayDirY1 = dirY + planeY

    posZ = 0.5 * h  # altura da câmera para perspectiva

    for y in range(h // 2 + 1, h):
        p = y - h // 2
        rowDistance = posZ / p

        floorStepX = rowDistance * (rayDirX1 - rayDirX0) / w
        floorStepY = rowDistance * (rayDirY1 - rayDirY0) / w

        floorX = posX + rowDistance * rayDirX0
        floorY = posY + rowDistance * rayDirY0

        for x in range(w):
            cellX = int(floorX)
            cellY = int(floorY)

            # limita índices para não crashar
            cellX = min(max(cellX, 0), floor_map_w - 1)
            cellY = min(max(cellY, 0), floor_map_h - 1)

            tx = int(TEX_W * (floorX - cellX)) % TEX_W
            ty = int(TEX_H * (floorY - cellY)) % TEX_H

            floorX += floorStepX
            floorY += floorStepY

            # Floor
            checker = (cellX + cellY) & 1
            floorTex = floorDefaultTex1 if checker == 0 else floorDefaultTex2

            mapValue = floorMap[cellX, cellY]
            if mapValue == 0:
                floorTex = min(floorTex, num_textures - 1)
            else:
                floorTex = min(mapValue - 1, num_textures - 1)


            color = textures[floorTex+floor_tex_sum, ty, tx]
            buffer_out[y, x] = (color >> 1) & 8355711  # escurece

            # Ceiling
            mapValue = ceilMap[cellX, cellY]
            if mapValue == 0:
                ceilTex = min(ceilDefaultTex, num_textures + ceil_tex_sum)
            else:
                ceilTex = min(mapValue + ceil_tex_sum, num_textures + ceil_tex_sum)

            color = textures[ceilTex, ty, tx]
            buffer_out[h - y - 1, x] = (color >> 1) & 8355711


    