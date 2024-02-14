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
        
        # Add sphere mesh model
        add (
            Sphere(app, pos=(2, 2, 0))
        )
            
    def render(self):
        for object in self.objects:
            object.render()
        self.skybox.render()