from engine.ecs.components.all import SimpleAnimation, StateAnimation, States, Texture
from engine.utils.scaler import scaler

#================================#
class SimpleAnimationSystem:
    #--------------------------------#
    def __init__(self, world:object):
        #--------------------------------#
        self.on_screen:bool = False
        self.world = world

    #================================#
    def update(self, dt):
        #--------------------------------#
        for entity, (animation, texture) in self.world.query(SimpleAnimation,Texture):
            #--------------------------------#
            animation.timer += dt
            #--------------------------------#
            if animation.timer >= animation.frame_time:
                #--------------------------------#
                animation.timer -= animation.frame_time
                #--------------------------------#
                animation.current_frame += 1
                #--------------------------------#
                if animation.current_frame >= len(animation.textures):
                    animation.current_frame = 0
                #--------------------------------#
                texture.texture = animation.textures[
                    animation.current_frame
                ]
                texture.original_texture = animation.textures[
                    animation.current_frame]

#================================#
class StateAnimationSystem:
    #--------------------------------#
    def __init__(self, world:object):
        #--------------------------------#
        self.on_screen:bool = False
        self.world = world

    #================================#
    def update(self, dt):
        #--------------------------------#
        for entity, (animation, states, texture) in self.world.query(StateAnimation, States, Texture):
            #--------------------------------#
            current = states.current
            #--------------------------------#
            ani = animation.states.get(current)
            #--------------------------------#
            animation.timer += dt
            #--------------------------------#
            if animation.timer >= ani.frame_time:
                #--------------------------------#
                animation.timer -= ani.frame_time
                #--------------------------------#
                animation.current_frame += 1
                #--------------------------------#
                if animation.current_frame >= len(ani.textures):
                    animation.current_frame = 0
                #--------------------------------#
                texture.texture = ani.textures[
                    animation.current_frame
                ]
                texture.original_texture = ani.textures[
                    animation.current_frame
                ]


                