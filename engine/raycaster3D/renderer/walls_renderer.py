from numba import njit
import numpy as np
import math
from engine.configs.configs import configs


thin_wall_tex_sum = np.int32(0)#settings.get("raycast_thin_wall_tex_sum", 0))
door_tex_sum = np.int32(0)#settings.get("raycast_door_tex_sum", 0))
wall_tex_sum = np.int32(0)#settings.get("raycast_wall_tex_sum", 0))

@njit(fastmath=True)
def check_thin_walls(posX, posY, rayDirX, rayDirY, thin_walls):
    closest_dist = 1e30
    hit_tex = -1
    hit_index = -1
    hit_side = 0
    wallX = 0.0

    for i in range(thin_walls.shape[0]):
        wx = thin_walls[i, 0]
        wy = thin_walls[i, 1]

        wtype = int(thin_walls[i, 2])
        thickness = thin_walls[i, 3]
        tex = int(thin_walls[i, 4])

        if wtype == 0:
            if rayDirX == 0:
                continue

            t = (wx - posX) / rayDirX

            if t <= 0:
                continue

            y_hit = posY + t * rayDirY

            if abs(y_hit - wy) <= thickness * 0.5:
                if t < closest_dist:
                    closest_dist = t
                    hit_tex = tex + thin_wall_tex_sum
                    hit_index = i
                    hit_side = 0
                    wallX = y_hit - math.floor(y_hit)

        else:
            if rayDirY == 0:
                continue

            t = (wy - posY) / rayDirY

            if t <= 0:
                continue

            x_hit = posX + t * rayDirX

            if abs(x_hit - wx) <= thickness * 0.5:
                if t < closest_dist:
                    closest_dist = t
                    hit_tex = tex + thin_wall_tex_sum
                    hit_index = i
                    hit_side = 1
                    wallX = x_hit - math.floor(x_hit)

    return hit_tex, closest_dist, hit_index, hit_side, wallX

@njit(fastmath=True)
def check_doors(posX, posY, rayDirX, rayDirY, doors):
    closest_dist = 1e30
    hit_tex = -1
    hit_index = -1
    hit_side = 0
    wallX = 0.0

    for i in range(doors.shape[0]):
        x = doors[i, 0]
        y = doors[i, 1]
        wtype = int(doors[i, 2])
        width = doors[i, 3]
        tex = int(doors[i, 4])
        offset = doors[i, 5]
        
        if wtype == 0:

            door_y = y + offset

            if abs(rayDirX) < 1e-8:
                continue

            t = (x - posX) / rayDirX

            if t <= 0:
                continue

            y_hit = posY + t * rayDirY

            if abs(y_hit - door_y) <= width * 0.5:

                if t < closest_dist:
                    closest_dist = t
                    hit_tex = tex + door_tex_sum
                    hit_index = i
                    hit_side = 0

                    wallX = y_hit - door_y
                    wallX -= math.floor(wallX)
        else:

            door_x = x + offset

            if abs(rayDirY) < 1e-8:
                continue

            t = (y - posY) / rayDirY

            if t <= 0:
                continue

            x_hit = posX + t * rayDirX

            if abs(x_hit - door_x) <= width * 0.5:

                if t < closest_dist:
                    closest_dist = t
                    hit_tex = tex + door_tex_sum
                    hit_index = i
                    hit_side = 1

                    wallX = x_hit - door_x
                    wallX -= math.floor(wallX)

    return (
        hit_tex,
        closest_dist,
        hit_index,
        hit_side,
        wallX
    )

@njit(fastmath=True)
def render_walls(
    posX, posY, dirX, dirY, planeX, planeY,
    worldMap,
    textures,
    buffer_out,
    ZBuffer,
    thin_walls,
    doorsMap,
    TEX_W=32, TEX_H=32
):
    h, w = buffer_out.shape
    tex_sum = wall_tex_sum

    for x in range(w):

        cameraX = 2 * x / w - 1
        rayDirX = dirX + planeX * cameraX
        rayDirY = dirY + planeY * cameraX

        mapX = int(posX)
        mapY = int(posY)

        deltaDistX = abs(1 / rayDirX) if rayDirX != 0 else 1e30
        deltaDistY = abs(1 / rayDirY) if rayDirY != 0 else 1e30

        if rayDirX < 0:
            stepX = -1
            sideDistX = (posX - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX + 1.0 - posX) * deltaDistX

        if rayDirY < 0:
            stepY = -1
            sideDistY = (posY - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY + 1.0 - posY) * deltaDistY

        hit = 0
        side = 0

        # ===== DDA =====
        while hit == 0:
            if sideDistX < sideDistY:
                sideDistX += deltaDistX
                mapX += stepX
                side = 0
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1

            if worldMap[mapX, mapY] > 0:
                hit = 1

        # distância parede normal
        if side == 0:
            perpWallDist = (mapX - posX + (1 - stepX) / 2) / rayDirX
        else:
            perpWallDist = (mapY - posY + (1 - stepY) / 2) / rayDirY

        texNum = worldMap[mapX, mapY] + tex_sum

        # ===== THIN WALL CHECK =====
        thin_tex, thin_dist, thin_index, thin_side, thin_wallX = check_thin_walls(
            posX, posY, rayDirX, rayDirY, thin_walls
        )

        if thin_tex != -1 and thin_dist < perpWallDist:
            perpWallDist = thin_dist
            texNum = thin_tex
            side = thin_side
            wallX = thin_wallX
        else:
            if side == 0:
                wallX = posY + perpWallDist * rayDirY
            else:
                wallX = posX + perpWallDist * rayDirX
            wallX -= math.floor(wallX)

        # ===== door_check =====
        door_tex, door_dist, door_index, door_side, door_wallX = check_doors(
            posX, posY, rayDirX, rayDirY, doorsMap
        )
        if door_tex != -1 and door_dist < perpWallDist:
            perpWallDist = door_dist
            texNum = door_tex
            side = door_side
            wallX = door_wallX

        # ===== altura da linha =====
        lineHeight = int(h / (perpWallDist + 1e-6))

        drawStart = -lineHeight // 2 + h // 2
        if drawStart < 0:
            drawStart = 0

        drawEnd = lineHeight // 2 + h // 2
        if drawEnd >= h:
            drawEnd = h - 1

        texX = int(wallX * TEX_W)
        if side == 0 and rayDirX > 0:
            texX = TEX_W - texX - 1
        if side == 1 and rayDirY < 0:
            texX = TEX_W - texX - 1

        step = TEX_H / lineHeight
        texPos = (drawStart - h / 2 + lineHeight / 2) * step

        for y in range(drawStart, drawEnd):
            texY = int(texPos) & (TEX_H - 1)
            texPos += step

            color = textures[texNum, texY, texX]

            if side == 1:
                color = (color >> 1) & 8355711

            buffer_out[y, x] = color

        ZBuffer[x] = perpWallDist

        