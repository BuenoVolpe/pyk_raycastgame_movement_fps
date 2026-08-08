from numba import njit
import math
import numpy as np
from engine.configs.configs import configs
from engine.raycaster3D.renderer.walls_renderer import check_doors, check_thin_walls


HIT_NONE = 0
HIT_WALL = 1
HIT_THIN_WALL = 2
HIT_DOOR = 3
HIT_SPRITE = 4


@njit(fastmath=True)
def pick_entity(
    posX, posY,
    dirX, dirY,
    planeX, planeY,
    worldMap,
    thin_walls,
    doors,
    sprites,
    zbuffer
):
    # =========================================================
    # RAIO CENTRAL
    # =========================================================

    rayDirX = dirX
    rayDirY = dirY

    mapX = int(posX)
    mapY = int(posY)

    deltaDistX = abs(1.0 / rayDirX) if rayDirX != 0 else 1e30
    deltaDistY = abs(1.0 / rayDirY) if rayDirY != 0 else 1e30

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

    # =========================================================
    # DDA DA PAREDE
    # =========================================================

    while hit == 0:

        if sideDistX < sideDistY:
            sideDistX += deltaDistX
            mapX += stepX
            side = 0
        else:
            sideDistY += deltaDistY
            mapY += stepY
            side = 1

        # segurança
        if (
            mapX < 0 or
            mapY < 0 or
            mapY >= worldMap.shape[0] or
            mapX >= worldMap.shape[1]
        ):
            break

        if worldMap[mapX, mapY] > 0:
            hit = 1

    if hit == 1:

        if side == 0:
            wallDist = (
                mapX - posX + (1 - stepX) * 0.5
            ) / rayDirX
        else:
            wallDist = (
                mapY - posY + (1 - stepY) * 0.5
            ) / rayDirY

    else:
        wallDist = 1e30

    (
        thin_tex,
        thin_dist,
        thin_index,
        thin_side,
        thin_wallX
    ) = check_thin_walls(
        posX,
        posY,
        rayDirX,
        rayDirY,
        thin_walls
    )

    (
        door_tex,
        door_dist,
        door_index,
        door_side,
        door_wallX
    ) = check_doors(
        posX,
        posY,
        rayDirX,
        rayDirY,
        doors
    )

    interaction_door_index = -1
    interaction_door_dist = 1e30
    closest_dist = wallDist
    hit_type = HIT_WALL
    hit_index = -1
    hit_eid = -1


    for i in range(doors.shape[0]):

        x = doors[i, 0]
        y = doors[i, 1]

        width = doors[i, 3]

        dx = x - posX
        dy = y - posY

        forward = dx * rayDirX + dy * rayDirY

        if forward <= 0:
            continue

        hit_x = posX + rayDirX * forward
        hit_y = posY + rayDirY * forward

        distance_from_ray = math.sqrt(
            (x - hit_x) * (x - hit_x) +
            (y - hit_y) * (y - hit_y)
        )

        interaction_radius = width * 0.5 + 0.25

        if distance_from_ray <= interaction_radius:

            if forward < interaction_door_dist:
                interaction_door_dist = forward
                interaction_door_index = i

    if thin_tex != -1 and thin_dist < closest_dist:
        closest_dist = thin_dist
        hit_type = HIT_THIN_WALL
        hit_index = thin_index
        hit_eid = int(thin_walls[thin_index, 6])

    if interaction_door_index != -1:

        if interaction_door_dist < closest_dist:

            hit_type = HIT_DOOR
            hit_index = interaction_door_index
            hit_eid = int(doors[interaction_door_index, 10])
            closest_dist = interaction_door_dist


    closest_sprite_dist = 1e30
    closest_sprite_index = -1

    for i in range(sprites.shape[0]):

        sx = sprites[i, 0]
        sy = sprites[i, 1]
        scale = sprites[i, 3]

        dx = sx - posX
        dy = sy - posY

        # distância ao longo do raio
        forward_dist = dx * rayDirX + dy * rayDirY

        if forward_dist <= 0:
            continue

        # ponto mais próximo do sprite sobre o raio
        closest_x = posX + rayDirX * forward_dist
        closest_y = posY + rayDirY * forward_dist

        distance_from_ray = math.sqrt(
            (sx - closest_x) * (sx - closest_x) +
            (sy - closest_y) * (sy - closest_y)
        )

        # raio aproximado do sprite
        radius = 0.5 * scale

        if distance_from_ray <= radius:

            if forward_dist < closest_sprite_dist:
                closest_sprite_dist = forward_dist
                closest_sprite_index = i

    if closest_sprite_index != -1:

        sprite_dist = closest_sprite_dist

        if sprite_dist < closest_dist:

            # também compara com zbuffer central
            center_x = zbuffer.shape[0] // 2

            if sprite_dist < zbuffer[center_x]:

                hit_type = HIT_SPRITE
                hit_index = closest_sprite_index
                hit_eid = int(sprites[closest_sprite_index, 5])
                closest_dist = sprite_dist

    return hit_type, hit_index, hit_eid, closest_dist
    


