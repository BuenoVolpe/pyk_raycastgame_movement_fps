from engine.ecs.components.all import Velocity, Position, AngularMovementTag, Angle, Camera3D, Direction, CollisionTag
from engine.utils.scaler import scaler
import math
#================================#
class MovementSystem:
    #--------------------------------#
    def __init__(self, world:object):
        #--------------------------------#
        self.world = world

    #================================#
    def update(self, dt):
        #--------------------------------#
        for entity, (velocity, position) in self.world.query(Velocity, Position, exclude=(AngularMovementTag, Camera3D,CollisionTag)):
            if not velocity.can_move:
                continue
            #--------------------------------#
            position.x += velocity.x * dt
            position.y += velocity.y * dt
            #
            # --------------------------------#
            position.pos.update(
                position.x,
                position.y
            )
#================================#
class AngularMovementSystem:
    #--------------------------------#
    def __init__(self, world:object):
        #--------------------------------#
        self.world = world

    #================================#
    def update(self, dt):
        #--------------------------------#
        for entity, (vel, pos, direction, tag) in self.world.query(
            Velocity, Position, Direction, AngularMovementTag, exclude=(Camera3D,CollisionTag)
            ):
            if not vel.can_move:
                continue    
            self.move_with_direction(entity, vel, pos, direction, dt)
        #--------------------------------#
        for entity, (vel, pos, angle, tag) in self.world.query(
            Velocity, Position, Angle, AngularMovementTag, exclude=(Direction,)
        ):
            if not vel.can_move:
                continue    
            self.move_without_direction(entity, angle, vel, pos, dt)
    #================================#
    def move_with_direction(self, entity, vel, pos, direction, dt):
        #--------------------------------#
        # Forward
        fx = direction.x
        fy = direction.y
        #--------------------------------#
        # Right (90°)
        rx = -fy
        ry = fx
        vel_y = -vel.y
        #--------------------------------#
        pos.x += (fx * vel_y + rx * vel.x) * dt
        pos.y += (fy * vel_y + ry * vel.x) * dt
        #--------------------------------#
        pos.pos.update(pos.x, pos.y)
        
    #================================#
    def move_without_direction(self, entity, angle, velocity, position, dt):
        #--------------------------------#
        direction_x = math.cos(math.radians(angle.angle))
        direction_y = math.sin(math.radians(angle.angle))
        #--------------------------------#
        position.x += direction_x * velocity.x * dt
        position.y += direction_y * velocity.x * dt
        #--------------------------------#
        position.pos.update(
            position.x,
            position.y
        )
            
