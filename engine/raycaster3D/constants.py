#---imports---#
from dataclasses import dataclass
import numpy as np
from engine.configs.configs import configs
#---settings---#
SCREEN_W = configs.game.base_window_width
SCREEN_H = configs.game.base_window_height
TEX_W = configs.game.raytexture_size      
TEX_H = configs.game.raytexture_size          
#---FRAMEBUFFER and ZBUFFER---#
buffer = np.zeros((SCREEN_H, SCREEN_W), dtype=np.uint32)  # screen buffer
ZBuffer = np.zeros(SCREEN_W, dtype=np.float64)   # walls distance
#---initial player positions---#
posX, posY = 22.0, 11.5
dirX, dirY = -1.0, 0.0 # initial direction
planeX, planeY = 0.0, 0.66 # camera plane

HIT_NONE = 0
HIT_WALL = 1
HIT_THIN_WALL = 2
HIT_DOOR = 3
HIT_SPRITE = 4
#---world map---#
worldMap_list = [
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
]
worldMap = np.array(worldMap_list, dtype=np.int32)
#---settings part 2---#
MAP_H = len(worldMap_list)
MAP_W = len(worldMap_list[0])
#---sprite class---#
# @dataclass
# class Sprite:
#     x: float        #postions
#     y: float        #postions
#     texture: int    #texture index
#---sprite list---#
sprites = np.array([ #(x, y, texture, scale, offsetZ, eid)
    [20.5, 11.5, 10, 1, 0, -1],
    [18.5, 4.5, 10, .5, 0.6, -1],
    [10.0, 4.5, 10, 1, 0, -1],
    [10.0, 12.5,10, 1, 0, -1],
    [3.5,  6.5, 10, 1, 0, -1],
    [3.5,  20.5,10, 1, 0, -1],
    [3.5,  14.5,10, 1, 0, -1],
    [14.5,20.5,10, 1, 0, -1],
    [18.5, 10.5, 9, 1, 0, -1],
    [18.5, 11.5, 9, 1, 0, -1],
    [18.5, 12.5, 9, 1, 0, -1],
    [21.5, 1.5, 8, 1, 0, -1],
    [15.5, 1.5, 8, 1, 0, -1],
    [16.0, 1.8, 8, 1, 0, -1],
    [16.2, 1.2, 8, 1, 0, -1],
    [3.5,  2.5, 8, 1, 0, -1],
    [9.5, 15.5, 8, 1, 0, -1],
    [10.0, 15.1,8, 1, 0, -1],
    [10.5, 15.8,8, 1, 0, -1],
], dtype=np.float64)

NUM_SPRITES = sprites.shape[0]

#* x, y, tipo[0v, 1h], espessura, textura, colisão?, eid
# default_thin_walls = np.array([
# ], dtype=np.float64)
default_thin_walls = np.empty((0, 7), dtype=np.float64)

# default_doors = np.array([
# ], dtype=np.float64)
#* x, y, tipo, largura, tex, offset(qnt abriu), speed, open_state, H?, H_texture
default_doors = np.empty((0, 11), dtype=np.float64)

# --- sprites ---
# default_sprites_data = np.array([
# ], dtype=np.float64)
#* x, y, tex, scale, offsetZ, flags
default_sprites_data = np.empty((0, 6), dtype=np.float64)


