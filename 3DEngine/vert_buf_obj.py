import numpy as np
import moderngl as mgl
import pywavefront

class VertexBufferObject:
    def __init__(self, ctx):
        self.vert_buf_objs = {}
        self.vert_buf_objs['cube'] = CubeVertexBufferObject(ctx)
        self.vert_buf_objs['cat'] = CatVertexBufferObject(ctx)
        self.vert_buf_objs['sphere'] = SphereVertexBufferObject(ctx)
        self.vert_buf_objs['skybox'] = SkyBoxVertexBufferObject(ctx)
        self.vert_buf_objs['advanced_skybox'] = AdvancedSkyBoxVertexBufferObject(ctx)

    def destroy(self):
        [vert_buf_obj.destroy() for vert_buf_obj in self.vert_buf_objs.values()]

class BaseVertexBufferObject:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vert_buf_obj = self.get_vertex_buffer_object()
        self.format: str = None
        self.attribs: list = None

    def get_vertex_data(self): ...

    def get_vertex_buffer_object(self):
        vertex_data = self.get_vertex_data()
        vert_buf_obj = self.ctx.buffer(vertex_data)
        return vert_buf_obj

    def destroy(self):
        self.vert_buf_obj.release()


class CubeVertexBufferObject(BaseVertexBufferObject):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    @staticmethod
    def get_data(vertices, faces):
        data = [vertices[index] for face in faces for index in face]
        return np.array(data, dtype='f4')

    def get_vertex_data(self):
        vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]

        faces = [(0, 2, 3), (0, 1, 2),
                (1, 7, 2), (1, 6, 7),
                (6, 5, 4), (4, 7, 6),
                (3, 4, 5), (3, 5, 0),
                (3, 7, 4), (3, 2, 7),
                (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, faces)

        texture_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        texture_coord_faces = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1),]
        texture_coord_data = self.get_data(texture_coord_vertices, texture_coord_faces)

        normals = [( 0, 0, 1) * 6,
                   ( 1, 0, 0) * 6,
                   ( 0, 0,-1) * 6,
                   (-1, 0, 0) * 6,
                   ( 0, 1, 0) * 6,
                   ( 0,-1, 0) * 6]
        normals = np.array(normals, dtype='f4').reshape(36, 3)

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([texture_coord_data, vertex_data])
        return vertex_data


class CatVertexBufferObject(BaseVertexBufferObject):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
        
    def get_vertex_data(self):
        objects = pywavefront.Wavefront('objects/20430_Cat_v1_NEW.obj', cache=True, parse=True)
        object = objects.materials.popitem()[1]
        vertex_data = object.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
    
class SphereVertexBufferObject(BaseVertexBufferObject):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
        
    @staticmethod
    def get_data(vertices, faces):
        data = [vertices[index] for face in faces for index in face]
        return np.array(data, dtype='f4')
    
    def read_npz(self, data):
        vertices = [(x[0], x[1], x[2]) for x in data['verts']]
        faces = [(x[0], x[1], x[2]) for x in data['faces']]
        return vertices, faces
        
    def get_vertex_data(self):
        data = np.load('objects/sphere.npz')
        vertices, faces = self.read_npz(data)
        vertex_data = np.array([vertices[index] for face in faces for index in face], dtype='f4')
        return vertex_data
        

class SkyBoxVertexBufferObject(BaseVertexBufferObject):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '3f'
        self.attribs = ['in_position']

    @staticmethod
    def get_data(vertices, faces):
        data = [vertices[index] for face in faces for index in face]
        return np.array(data, dtype='f4')

    def get_vertex_data(self):
        vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]

        faces = [(0, 2, 3), (0, 1, 2),
                (1, 7, 2), (1, 6, 7),
                (6, 5, 4), (4, 7, 6),
                (3, 4, 5), (3, 5, 0),
                (3, 7, 4), (3, 2, 7),
                (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, faces)
        vertex_data = np.flip(vertex_data, 1).copy(order='C')
        return vertex_data
    
    

class AdvancedSkyBoxVertexBufferObject(BaseVertexBufferObject):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '3f'
        self.attribs = ['in_position']

    def get_vertex_data(self):
        # in clip space
        z = 0.9999
        vertices = [(-1, -1, z), (3, -1, z), (-1, 3, z)]
        vertex_data = np.array(vertices, dtype='f4')
        return vertex_data