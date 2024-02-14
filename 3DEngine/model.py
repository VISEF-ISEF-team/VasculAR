import numpy as np
import glm
import pygame as pg


class Cube:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.ver_buf_obj = self.get_vertex_buffer_object()
        self.shader_program = self.get_shader_program('default')
        self.ver_arr_obj = self.get_vertex_array_objects()
        self.matrix_model = self.get_model_matrix()
        self.texture = self.get_texture(path='textures/wood.png')
        self.on_init()
        
    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        return texture
        
    def update(self):
        matrix_model = glm.rotate(self.matrix_model, self.app.time * 0.5, glm.vec3(0, 1, 0))
        self.shader_program['matrix_model'].write(matrix_model)
        self.shader_program['matrix_view'].write(self.app.camera.matrix_view)
        self.shader_program['camPos'].write(self.app.camera.position)
         
    def get_model_matrix(self):
        matrix_model = glm.mat4()
        return matrix_model     
         
    def on_init(self):
        # light
        self.shader_program['light.position'].write(self.app.light.position)
        self.shader_program['light.Ia'].write(self.app.light.Ia)
        self.shader_program['light.Id'].write(self.app.light.Id)
        self.shader_program['light.Is'].write(self.app.light.Is)
        
        # texture
        self.shader_program['u_texture_0'] = 0
        self.texture.use()
        
        # mvp
        self.shader_program['matrix_projection'].write(self.app.camera.matrix_projection)
        self.shader_program['matrix_view'].write(self.app.camera.matrix_view)
        self.shader_program['matrix_model'].write(self.matrix_model)
    
    def get_vertex_array_objects(self):
        ver_arr_obj = self.ctx.vertex_array(self.shader_program, [
            (self.ver_buf_obj, '2f 3f 3f', 'in_texcoord_0', 'in_normal', 'in_position')
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
        
        texture_coord = [(0,0), (1,0), (1,1), (0,1)]
        texture_coord_faces= [
            (0, 2, 3), (0, 1, 2),
            (0, 2, 3), (0, 1, 2),
            (0, 1, 2), (2, 3, 0),
            (2, 3, 0), (2, 0, 1),
            (0, 2, 3), (0, 1, 2),
            (3, 1, 2), (3, 0, 1),
        ]
        texture_coord_data = self.get_data(texture_coord, texture_coord_faces)
        
        normals = [
            (0, 0, 1) * 6,
            (1, 0, 0) * 6,
            (0, 0, -1) * 6,
            (-1, 0, 0) * 6,
            (0, 1, 0) * 6,
            (0, -1, 0) * 6
        ]
        normals = np.array(normals, dtype='f4').reshape(36, 3)
        
        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([texture_coord_data, vertex_data])
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