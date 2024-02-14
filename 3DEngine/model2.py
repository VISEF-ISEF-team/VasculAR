import moderngl as mgl
import numpy as np
import glm


class BaseModel:
    def __init__(self, app, vert_arr_obj_name, texture_id):
        self.app = app
        self.matrix_model = self.get_model_matrix()
        self.texture_id = texture_id
        self.vert_arr_obj_name = app.mesh.vert_arr_obj.vert_arr_objs[vert_arr_obj_name]
        self.program = self.vert_arr_obj_name.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        matrix_model = glm.mat4()
        return matrix_model

    def render(self):
        self.update()
        self.vao.render()


class Cube(BaseModel):
    def __init__(self, app, vert_arr_obj_name='cube', texture_id=0):
        super().__init__(app, vert_arr_obj_name, texture_id)
        self.on_init()

    def update(self):
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['matrix_view'].write(self.camera.matrix_view)
        self.program['matrix_model'].write(self.matrix_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        
        # mvp
        self.program['matrix_projetion'].write(self.camera.matrix_projetion)
        self.program['matrix_view'].write(self.camera.matrix_view)
        self.program['matrix_model'].write(self.matrix_model)
        
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)