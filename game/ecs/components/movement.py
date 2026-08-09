import pygame as pg
import numpy as np
import math
#================================#
from engine.ecs.component_storage import register_game_component
#--------------------------------#
from engine.utils.globalclasses import globalclasses
#================================#
@register_game_component
class GroundMovement:

    def __init__(
        self,
        acceleration=10.0,
        air_acceleration=10.0,
        friction=4.0,
        stop_speed=100.0,
        air_speed_cap=30.0,
        player_friction=1.0,
        grounded=True
    ):
        self.acceleration = acceleration
        self.air_acceleration = air_acceleration
        self.friction = friction
        self.stop_speed = stop_speed
        self.air_speed_cap = air_speed_cap
        self.player_friction = player_friction
        self.grounded = grounded
