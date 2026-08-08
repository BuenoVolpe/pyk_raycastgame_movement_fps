#---imports---#
import math
from sys import exit, executable, argv
from os import execv
import time
from dataclasses import dataclass

import numpy as np
import pygame
from numba import njit, prange

from colorama import Fore, Style, init
#---settings---#
SCREEN_W = 640
SCREEN_H = 480
TEX_W = 64      
TEX_H = 64      
MAP_W = 24      
MAP_H = 24      
#---world map---#
worldMap = np.array([
  [8,8,8,8,8,8,8,8,8,8,8,4,4,6,4,4,6,4,6,4,4,4,6,4],
  [8,0,0,0,0,0,0,0,0,0,8,4,0,0,0,0,0,0,0,0,0,0,0,4],
  [8,0,3,3,0,0,0,0,0,8,8,4,0,0,0,0,0,0,0,0,0,0,0,6],
  [8,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
  [8,0,3,3,0,0,0,0,0,8,8,4,0,0,0,0,0,0,0,0,0,0,0,4],
  [8,0,0,0,0,0,0,0,0,0,8,4,0,0,0,0,0,6,6,6,0,6,4,6],
  [8,8,8,8,0,8,8,8,8,8,8,4,4,4,4,4,4,6,0,0,0,0,0,6],
  [7,7,7,7,0,7,7,7,7,0,8,0,8,0,8,0,8,4,0,4,0,6,0,6],
  [7,7,0,0,0,0,0,0,7,8,0,8,0,8,0,8,8,6,0,0,0,0,0,6],
  [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,6,0,0,0,0,0,4],
  [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,6,0,6,0,6,0,6],
  [7,7,0,0,0,0,0,0,7,8,0,8,0,8,0,8,8,6,4,6,0,6,6,6],
  [7,7,7,7,0,7,7,7,7,8,8,4,0,6,8,4,8,3,3,3,0,3,3,3],
  [2,2,2,2,0,2,2,2,2,4,6,4,0,0,6,0,6,3,0,0,0,0,0,3],
  [2,2,0,0,0,0,0,2,2,4,0,0,0,0,0,0,4,3,0,0,0,0,0,3],
  [2,0,0,0,0,0,0,0,2,4,0,0,0,0,0,0,4,3,0,0,0,0,0,3],
  [1,0,0,0,0,0,0,0,1,4,4,4,4,4,6,0,6,3,3,0,0,0,3,3],
  [2,0,0,0,0,0,0,0,2,2,2,1,2,2,2,6,6,0,0,5,0,5,0,5],
  [2,2,0,0,0,0,0,2,2,2,0,0,0,2,2,0,5,0,5,0,0,0,5,5],
  [2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,5,0,5,0,5,0,5,0,5],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5],
  [2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,5,0,5,0,5,0,5,0,5],
  [2,2,0,0,0,0,0,2,2,2,0,0,0,2,2,0,5,0,5,0,0,0,5,5],
  [2,2,2,2,1,2,2,2,2,2,2,1,2,2,2,5,5,5,5,5,5,5,5,5]
], dtype=np.int32)
#---sprite class---#
@dataclass
class Sprite:
    x: float        #postions
    y: float        #postions
    texture: int    #texture index
#---sprite list---#
sprites = np.array([ #(x, y, texture)
    (20.5, 11.5, 10),
    (18.5, 4.5, 10),
    (10.0, 4.5, 10),
    (10.0, 12.5,10),
    (3.5,  6.5, 10),
    (3.5,  20.5,10),
    (3.5,  14.5,10),
    (14.5,20.5,10),
    (18.5, 10.5, 9),
    (18.5, 11.5, 9),
    (18.5, 12.5, 9),
    (21.5, 1.5, 8),
    (15.5, 1.5, 8),
    (16.0, 1.8, 8),
    (16.2, 1.2, 8),
    (3.5,  2.5, 8),
    (9.5, 15.5, 8),
    (10.0, 15.1,8),
    (10.5, 15.8,8),
], dtype=np.float64)

NUM_SPRITES = sprites.shape[0]

#---auxiliar functions---#
def load_texture(path):
    """
    Loads an image as a texture:
    - converts to a uint32 array in the format 0xRRGGBB
    """
    surf = pygame.image.load(path).convert_alpha()      # carrega imagem com alfa
    surf = pygame.transform.scale(surf, (TEX_W, TEX_H))  # redimensiona
    arr = pygame.surfarray.pixels3d(surf).copy()        # array (w,h,3)
    arr = np.transpose(arr, (1,0,2)).astype(np.uint8)  # para (h,w,3)
    rgb32 = (arr[:,:,0].astype(np.uint32) << 16) | \
            (arr[:,:,1].astype(np.uint32) << 8) | \
            arr[:,:,2].astype(np.uint32)
    return rgb32

def buffer_to_surface(buffer_uint32):
    """
    Convert uint32 buffer (0xRRGGBB) to Pygame Surface
    """
    r = ((buffer_uint32 >> 16) & 0xFF).astype(np.uint8)
    g = ((buffer_uint32 >> 8) & 0xFF).astype(np.uint8)
    b = (buffer_uint32 & 0xFF).astype(np.uint8)
    rgb = np.dstack((r,g,b))
    rgb_t = np.transpose(rgb, (1,0,2))  # Pygame espera (w,h,3)
    surf = pygame.surfarray.make_surface(rgb_t)
    return surf

#---main render function---#
@njit(fastmath=True)
def render_frame(posX, posY, dirX, dirY, planeX, planeY,
                 worldMap, textures, tex_count,
                 sprites_arr, num_sprites,
                 buffer_out, ZBuffer):
    """
    Renders a full frame:
    1. Floor and ceiling casting
    2. Wall casting
    3. Sprite casting
    """

    h, w = buffer_out.shape  # Frame height and width

    # --- FLOOR AND CEILING CASTING ---
    # Loop through each row of the bottom half of the screen (floor)
    for y in range(h//2 + 1, h):
        # Ray directions for the left and right side of the screen
        rayDirX0 = dirX - planeX
        rayDirY0 = dirY - planeY
        rayDirX1 = dirX + planeX
        rayDirY1 = dirY + planeY

        p = y - h // 2  # Vertical distance from the screen center
        posZ = 0.5 * h  # Camera height

        # Distance from the floor for the current row
        rowDistance = posZ / p

        # Step increments for moving across the floor horizontally
        floorStepX = rowDistance * (rayDirX1 - rayDirX0) / w
        floorStepY = rowDistance * (rayDirY1 - rayDirY0) / w

        # Starting position on the floor
        floorX = posX + rowDistance * rayDirX0
        floorY = posY + rowDistance * rayDirY0

        # Loop through each column
        for x in range(w):
            cellX = int(floorX)
            cellY = int(floorY)
            # Texture coordinates
            tx = int(TEX_W * (floorX - cellX)) & (TEX_W - 1)
            ty = int(TEX_H * (floorY - cellY)) & (TEX_H - 1)

            # Move floor position to the next pixel
            floorX += floorStepX
            floorY += floorStepY

            # Checkerboard pattern for floor texture
            checker = (cellX + cellY) & 1
            floorTexture = 3 if checker == 0 else 4
            ceilingTexture = 6

            # Floor color with darkening effect
            color = textures[floorTexture, ty, tx]
            color = (color >> 1) & 8355711
            buffer_out[y, x] = color

            # Ceiling color
            color = textures[ceilingTexture, ty, tx]
            color = (color >> 1) & 8355711
            buffer_out[h - y - 1, x] = color

    # --- WALL CASTING ---
    for x in range(w):
        # x-coordinate in camera space (-1 left, 1 right)
        cameraX = 2.0 * x / float(w) - 1.0
        # Ray direction for this column
        rayDirX = dirX + planeX * cameraX
        rayDirY = dirY + planeY * cameraX

        mapX = int(posX)
        mapY = int(posY)

        # Delta distances
        deltaDistX = 1e30 if rayDirX == 0 else abs(1.0 / rayDirX)
        deltaDistY = 1e30 if rayDirY == 0 else abs(1.0 / rayDirY)

        # Initial distance to the next side of the grid
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

        # DDA: traverse the grid until hitting a wall
        hit = 0
        side = 0
        while hit == 0:
            if sideDistX < sideDistY:
                sideDistX += deltaDistX
                mapX += stepX
                side = 0  # x-side
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1  # y-side
            if worldMap[mapX, mapY] > 0:
                hit = 1

        # Perpendicular distance to the wall
        perpWallDist = sideDistX - deltaDistX if side == 0 else sideDistY - deltaDistY
        if perpWallDist == 0: perpWallDist = 1e-6

        # Line height to draw
        lineHeight = int(h / perpWallDist)
        drawStart = max(-lineHeight // 2 + h // 2, 0)
        drawEnd = min(lineHeight // 2 + h // 2, h - 1)

        # Wall texture
        texNum = worldMap[mapX, mapY] - 1
        wallX = posY + perpWallDist * rayDirY if side == 0 else posX + perpWallDist * rayDirX
        wallX -= math.floor(wallX)
        texX = int(wallX * TEX_W)
        if (side == 0 and rayDirX > 0) or (side == 1 and rayDirY < 0):
            texX = TEX_W - texX - 1

        # Step in texture
        step = TEX_H / lineHeight
        texPos = (drawStart - h / 2 + lineHeight / 2) * step
        for y in range(drawStart, drawEnd + 1):
            texY = int(texPos) & (TEX_H - 1)
            texPos += step
            color = textures[texNum, texY, texX]
            # Darken the side walls
            if side == 1:
                color = (color >> 1) & 8355711
            buffer_out[y, x] = color

        # Store wall distance in z-buffer
        ZBuffer[x] = perpWallDist

    # --- SPRITE CASTING ---
    # Compute distance of each sprite
    spriteOrder = np.arange(num_sprites, dtype=np.int32)
    spriteDist = np.empty(num_sprites, dtype=np.float64)
    for i in range(num_sprites):
        dx = posX - sprites_arr[i,0]
        dy = posY - sprites_arr[i,1]
        spriteDist[i] = dx*dx + dy*dy

    # Sort sprites from farthest to nearest
    for i in range(num_sprites-1):
        maxidx = i
        for j in range(i+1, num_sprites):
            if spriteDist[j] > spriteDist[maxidx]:
                maxidx = j
        spriteDist[i], spriteDist[maxidx] = spriteDist[maxidx], spriteDist[i]
        spriteOrder[i], spriteOrder[maxidx] = spriteOrder[maxidx], spriteOrder[i]

    # Draw each sprite
    for i in range(num_sprites):
        sx = sprites_arr[spriteOrder[i],0] - posX
        sy = sprites_arr[spriteOrder[i],1] - posY
        invDet = 1.0 / (planeX * dirY - dirX * planeY)
        transformX = invDet * (dirY * sx - dirX * sy)
        transformY = invDet * (-planeY * sx + planeX * sy)
        if transformY <= 0.0001:
            continue

        spriteScreenX = int((w / 2) * (1 + transformX / transformY))
        spriteHeight = abs(int(h / transformY))
        drawStartY = max(-spriteHeight // 2 + h // 2, 0)
        drawEndY = min(spriteHeight // 2 + h // 2, h-1)
        spriteWidth = abs(int(h / transformY))
        drawStartX = max(-spriteWidth // 2 + spriteScreenX, 0)
        drawEndX = min(spriteWidth // 2 + spriteScreenX, w-1)
        texId = int(sprites_arr[spriteOrder[i],2])

        # Draw sprite pixel by pixel
        for stripe in range(drawStartX, drawEndX + 1):
            texX = int(256 * (stripe - (-spriteWidth / 2 + spriteScreenX)) * TEX_W / spriteWidth) // 256
            if transformY > 0 and stripe >= 0 and stripe < w and transformY < ZBuffer[stripe]:
                for y in range(drawStartY, drawEndY + 1):
                    d = (y) * 256 - h * 128 + spriteHeight * 128
                    texY = ((d * TEX_H) // spriteHeight) // 256
                    if 0 <= texY < TEX_H:
                        color = textures[texId, texY, texX]
                        # Ignore transparent pixels
                        if (color & 0x00FFFFFF) != 0:
                            buffer_out[y, stripe] = color

    return

#---main function---#
def main():
    pygame.init()  #iniciate pygame
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))  #create window
    pygame.display.set_caption("Raycaster (Python port)")
    clock = pygame.time.Clock()
    #---load textures---#
    tex_names = [
        "pics/eagle.png","pics/redbrick.png","pics/purplestone.png","pics/greystone.png",
        "pics/bluestone.png","pics/mossy.png","pics/wood.png","pics/colorstone.png",
        "pics/barrel.png","pics/pillar.png","pics/greenlight.png"
    ]
    num_textures = len(tex_names)
    textures = np.zeros((num_textures, TEX_H, TEX_W), dtype=np.uint32)
    for i, name in enumerate(tex_names):
        textures[i] = load_texture(name)
    #---FRAMEBUFFER and ZBUFFER---#
    buffer = np.zeros((SCREEN_H, SCREEN_W), dtype=np.uint32)  # screen buffer
    ZBuffer = np.zeros(SCREEN_W, dtype=np.float64)           # walls distance
    #---initial player positions---#
    posX, posY = 22.0, 11.5
    dirX, dirY = -1.0, 0.0         # initial direction
    planeX, planeY = 0.0, 0.66     # camera plane
    #
    running = True
    prev_time = time.time()
    delta_time = 0
    fps_font = pygame.font.SysFont("Consolas", 18)
    #---main loop---#
    while running:
        #---calculate delta time---#
        now = time.time()
        delta_time = now - prev_time
        if delta_time <= 0: delta_time = 1e-6
        prev_time = now
        moveSpeed = delta_time * 3.0  # move speed
        rotSpeed = delta_time * 2.0   # rot speed
        #---keys input---#
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LALT:
                    running = False
                elif ev.key == pygame.K_F5:
                    print(Fore.GREEN + Style.BRIGHT + "restart code...")
                    execv(executable, ['python'] + argv)

        keys = pygame.key.get_pressed()
        #---player movemenet---#
        #move forward
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            nx = posX + dirX * moveSpeed
            ny = posY + dirY * moveSpeed
            if worldMap[int(nx), int(posY)] == 0:
                posX = nx
            if worldMap[int(posX), int(ny)] == 0:
                posY = ny

        #move backward
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            nx = posX - dirX * moveSpeed
            ny = posY - dirY * moveSpeed
            if worldMap[int(nx), int(posY)] == 0:
                posX = nx
            if worldMap[int(posX), int(ny)] == 0:
                posY = ny

        #rotate right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            oldDirX = dirX
            dirX = dirX * math.cos(-rotSpeed) - dirY * math.sin(-rotSpeed)
            dirY = oldDirX * math.sin(-rotSpeed) + dirY * math.cos(-rotSpeed)
            oldPlaneX = planeX
            planeX = planeX * math.cos(-rotSpeed) - planeY * math.sin(-rotSpeed)
            planeY = oldPlaneX * math.sin(-rotSpeed) + planeY * math.cos(-rotSpeed)

        #rotate left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            oldDirX = dirX
            dirX = dirX * math.cos(rotSpeed) - dirY * math.sin(rotSpeed)
            dirY = oldDirX * math.sin(rotSpeed) + dirY * math.cos(rotSpeed)
            oldPlaneX = planeX
            planeX = planeX * math.cos(rotSpeed) - planeY * math.sin(rotSpeed)
            planeY = oldPlaneX * math.sin(rotSpeed) + planeY * math.cos(rotSpeed)

        #---frame render---#
        render_frame(posX, posY, dirX, dirY, planeX, planeY,
                     worldMap, textures, num_textures,
                     sprites, NUM_SPRITES, buffer, ZBuffer)

        surf = buffer_to_surface(buffer)
        screen.blit(surf, (0,0))
        #---fps counter---#
        fps = clock.get_fps()
        fps_s = fps_font.render(f"FPS: {fps:.0f}", True, (255,255,255))
        screen.blit(fps_s, (5,5))

        pygame.display.flip()
        clock.tick()


    pygame.quit()
    exit()


#---start app---#
if __name__ == "__main__":
    main()

    