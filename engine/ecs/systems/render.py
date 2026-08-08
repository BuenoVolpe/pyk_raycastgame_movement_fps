from engine.ecs.components.all import Texture, Position, CameraFocusTag, Sprite3DTag
from engine.utils.scaler import scaler
from engine.utils.globalclasses import globalclasses
#================================#
class RenderSystem:
    #--------------------------------#
    def __init__(self, world:object):
        #--------------------------------#
        self.on_screen:bool = False
        self.world = world
    #================================#
    def update(self, surface):
        #--------------------------------#
        for entity, (render, position) in self.world.query(Texture, Position, exclude=(Sprite3DTag, )):
            #--------------------------------#
            if isinstance(render.texture, str):
                render.texture = self.world.game.texture_handler.get(render.texture)
            #--------------------------------#
            if render.scale:
                render.texture = scaler.surface(render.texture, render.scale)
                render.scale = None
            #--------------------------------#
            texture = render.texture
            scale = render.scale
            pos = x, y = position.x, position.y
            #--------------------------------#
            camera = globalclasses.Camera

            x, y = camera.world_to_screen(
                position.x,
                position.y
            )

            surface.blit(texture, (x,y))
            #--------------------------------#
#================================#
class CameraSystem:
    #--------------------------------#
    def __init__(self, world):
        self.on_screen=False
        self.world = world
    #--------------------------------#
    def update(self, surface):
        #--------------------------------#
        for entity, (position, tag) in self.world.query(Position, CameraFocusTag):
            camera = globalclasses.Camera
            #--------------------------------#
            if camera.target is None:
                camera.target = entity
            #--------------------------------#
            if tag.IS_ON_SCREEN_CENTER:
                tex = self.world.get_component(
                    camera.target,
                    Texture
                )
                w,h = 0,0
                if hasattr(tex.texture, "get_size"):
                    w,h = tex.texture.get_size()
            #--------------------------------#
            camera.follow([position.x+w, position.y+h//2], surface)
            

