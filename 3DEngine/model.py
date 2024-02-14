import numpy as np
import glm

class Cube:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.ver_buf_obj = self.get_vertex_buffer_object()
        self.shader_program = self.get_shader_program('default')
        self.ver_arr_obj = self.get_vertex_array_objects()
        self.matrix_model = self.get_model_matrix()
        self.on_init()
        
    def update(self):
        matrix_model = glm.rotate(self.matrix_model, self.app.time, glm.vec3(0, 1, 0))
        self.shader_program['matrix_model'].write(matrix_model)
         
    def get_model_matrix(self):
        matrix_model = glm.mat4()
        return matrix_model     
         
    def on_init(self):
        self.shader_program['matrix_projection'].write(self.app.camera.matrix_projection)
        self.shader_program['matrix_view'].write(self.app.camera.matrix_view)
        self.shader_program['matrix_model'].write(self.matrix_model)
    
    def get_vertex_array_objects(self):
        ver_arr_obj = self.ctx.vertex_array(self.shader_program, [
            (self.ver_buf_obj, '3f', 'in_position')
        ])
        return ver_arr_obj
    
    def render(self):
        self.update()
        self.ver_arr_obj.render()
        
    def destroy(self):
        self.ver_buf_obj.release()
        self.shader_program.release()
        self.ver_arr_obj.release()
    
    def get_vertex_data(self):
        vectices = [
            (-1, -1, 1), (1, -1, 1), (1, 1, 1),(-1, 1, 1),
            (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1),
        ]
        faces = [
            (0, 2, 3), (0, 1, 2),
            (1, 7, 2), (1, 6, 7),
            (6, 5, 4), (4, 7 ,6),
            (3, 4, 5), (3, 5, 0),
            (3, 7, 4), (3, 2, 7),
            (0, 6, 1), (0, 5, 6)
        ]
        vertex_data = self.get_data(vectices, faces)
        return vertex_data
    
    @staticmethod
    def get_data(vertices, faces):
        data = [vertices[index] for triangle in faces for index in triangle]
        return np.array(data, dtype='f4')
        
        
    def get_vertex_buffer_object(self):
        vertex_data = self.get_vertex_data()
        ver_buf_obj = self.ctx.buffer(vertex_data)
        return ver_buf_obj
    
    def get_shader_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
            
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        
        program = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader,
        )
        return program