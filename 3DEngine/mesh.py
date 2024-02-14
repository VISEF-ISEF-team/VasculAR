from vert_arr_obj import VertexArrayObject
from texture import Texture

class Mesh:
    def __init__(self, app):
        self.app = app
        self.vert_arr_obj = VertexArrayObject(app.ctx)
        self.texture = Texture(app)

    def destroy(self):
        self.vert_arr_obj.destroy()
        self.texture.destroy()