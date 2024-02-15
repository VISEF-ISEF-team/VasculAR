from model2 import *

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        self.skybox = AdvancedSkybox(app)
        
    def add_object(self, object):
        self.objects.append(object)
        
    def load(self):
        app = self.app
        add = self.add_object
        
        # Add cubes playground
        length, step = 30, 2
        for x in range(-length, length, step):
            for z in range(-length, length, step):
                add(
                    Cube(app, pos=(x, -step, z))
                )

        # Add custom mesh model
        add(
            Cat(app, pos=(0, 0, 0), rot=(-90,0,0))
        )
        
        # moving cube
        self.moving_cube = MovingCube(app, pos=(0,6,8), scale=(3,3,3), texture_id=1)
        add(self.moving_cube)
        
    def update(self):
        self.moving_cube.rot.xyz = self.app.time