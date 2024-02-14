import pygame as pg
import moderngl as mgl
import sys
from model2 import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
import os

class GraphicsEngine:
    def __init__(self, win_size=(1600, 900)):
        
        pg.init()
        self.WIN_SIZE = win_size
        
        # Locate the screen
        # screen_width, screen_height = pg.display.Info().current_w, pg.display.Info().current_h
        # window_x = screen_width - self.WIN_SIZE[0]
        # window_y = screen_height - self.WIN_SIZE[1]*1.2
        # os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_x},{window_y}"
        
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.event.set_grab(True)
        pg.mouse.set_visible(True)

        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        
        self.light = Light()
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.scene = Scene(self)
        
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()
                
    def render(self):
        self.ctx.clear(color=(0, 0, 0))
        self.scene.render()
        pg.display.flip()
        
    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001
        
    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)
            
                
if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
