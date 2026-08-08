import math
from engine.ecs.components.all import Position, Velocity, GridCollider, Direction, AngularMovementTag, CollisionTag
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
#================================#
class GridCollisionSystem:
    def __init__(self, world, grid, thin_walls=None, doors=None):
        #--------------------------------#
        self.world = world
        self.grid = grid
        #--------------------------------#
        self.thin_walls = thin_walls
        self.doors = doors
        #--------------------------------#
        self.map_h = len(grid)
        self.map_w = len(grid[0])
        #--------------------------------#
        signal_bus.subscribe(signals.GRID_COLLISION_CHANGE_GRID, self.change_grid, priority=sig_prio.AFTER_LOAD)
    #================================#
    def update(self, dt):
        #--------------------------------#
        for entity, (pos, vel, collider, coltag) in self.world.query(Position, Velocity, GridCollider, CollisionTag, exclude=(AngularMovementTag,)):
            #--------------------------------#
            self.try_move(pos, vel, collider, vel.x * dt, vel.y * dt)
        for entity, (pos, vel, collider, direction, angtag, coltag) in self.world.query(Position, Velocity, GridCollider, Direction, AngularMovementTag, CollisionTag):
            #--------------------------------#
            dx, dy = self._camera_motion(direction, vel)
            self.try_move(pos, vel, collider, dx * dt, dy * dt)
            #--------------------------------#
    #================================#
    def _camera_motion(self, direction, vel):
        #--------------------------------#
        fx = direction.x
        fy = direction.y
        #--------------------------------#
        rx = -fy
        ry = fx
        #--------------------------------#
        forward = -vel.y
        strafe = vel.x
        #--------------------------------#
        dx = fx * forward + rx * strafe
        dy = fy * forward + ry * strafe
        #--------------------------------#
        return dx, dy
    #================================#
    def try_move(self, pos, vel, collider, dx, dy):
        #--------------------------------#
        r = collider.radius
        #--------------------------------#
        nx = pos.x + dx
        if self.is_free(nx, pos.y, r):
            pos.x = nx
        #--------------------------------#
        ny = pos.y + dy
        if self.is_free(pos.x, ny, r):
            pos.y = ny
        #--------------------------------#
    #================================#
    def is_free(self, x, y, r):
        #--------------------------------#
        if not self.is_empty(x, y):
            return False
        #--------------------------------#
        if self.check_thin_collision(x, y, r):
            return False
        #--------------------------------#
        if self.check_door_collision(x, y, r):
            return False
        #--------------------------------#
        return True
    #================================#
    def check_thin_collision(self, px, py, radius):
        #--------------------------------#
        if self.thin_walls is None:
            return False
        #--------------------------------#
        for wall in self.thin_walls:
            #--------------------------------#
            if not wall[5]:
                continue
            #--------------------------------#
            wx = wall[0]
            wy = wall[1]
            #--------------------------------#
            wall_orientation = int(wall[2])
            length = wall[3]
            #--------------------------------#
            if wall_orientation == 0:
                #--------------------------------#
                if abs(px - wx) < 0.1+radius:
                    #--------------------------------#
                    if abs(py - wy) < length * 0.5 + radius:
                        return True
            #--------------------------------#
            else:
                #--------------------------------#
                if abs(py - wy) < radius:
                    #--------------------------------#
                    if abs(px - wx) < length * 0.5 + radius:
                        return True
        #--------------------------------#
        return False
    def check_door_collision(self, px, py, radius):
        #--------------------------------#
        if self.doors is None:
            return False
        #--------------------------------#
        for door in self.doors:
            #--------------------------------#
            if door[7] in [2, 5]:
                return
            #--------------------------------#
            x = door[0]
            y = door[1]
            #--------------------------------#
            wall_orientation = int(door[2])
            #--------------------------------#
            width = door[3]
            #--------------------------------#
            offset = door[5]
            #--------------------------------#
            if wall_orientation == 0:
                #--------------------------------#
                door_x = x + offset
                #--------------------------------#
                if abs(px-door_x) < radius:
                    #--------------------------------#
                    if abs(py-y) < width*0.5 + radius:
                        return True
            else:
                #--------------------------------#
                door_y = y + offset
                #--------------------------------#
                if abs(py-door_y) < radius:
                    #--------------------------------#
                    if abs(px-x) < width*0.5 + radius:
                        return True
        #--------------------------------#
        return False
    #================================#
    def is_empty(self, x, y):
        tx = int(x)
        ty = int(y)
        if tx < 0 or ty < 0:
            return False
        if tx >= self.map_w or ty >= self.map_h:
            return False
        return self.grid[tx, ty] == 0
    #================================#
    def change_grid(self, new_grid, thin_walls=None, doors=None):
        self.grid = new_grid
        self.map_h = new_grid.shape[0]
        self.map_w = new_grid.shape[1]

        self.thin_walls = thin_walls
        self.doors = doors
    