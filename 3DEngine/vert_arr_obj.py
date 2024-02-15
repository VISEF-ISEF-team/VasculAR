from vert_buf_obj import VertexBufferObject
from shader_program import ShaderProgram

class VertexArrayObject:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vert_buf_obj = VertexBufferObject(ctx)
        self.program = ShaderProgram(ctx)
        self.vert_arr_objs = {}

        # cube vertex array object
        self.vert_arr_objs['cube'] = self.get_vertex_array_object(
            program=self.program.programs['default'],
            vert_buf_obj = self.vert_buf_obj.vert_buf_objs['cube']
        )
        
        # shadow cube vertex array object
        self.vert_arr_objs['shadow_cube'] = self.get_vertex_array_object(
            program=self.program.programs['shadow_map'],
            vert_buf_obj = self.vert_buf_obj.vert_buf_objs['cube']
        )

        # cat vertex array object
        self.vert_arr_objs['cat'] = self.get_vertex_array_object(
            program=self.program.programs['default'],
            vert_buf_obj = self.vert_buf_obj.vert_buf_objs['cat']
        )
        
        # shadow cat vertex array object
        self.vert_arr_objs['shadow_cat'] = self.get_vertex_array_object(
            program=self.program.programs['shadow_map'],
            vert_buf_obj = self.vert_buf_obj.vert_buf_objs['cat']
        )
        
        # skybox vertex array object
        self.vert_arr_objs['skybox'] = self.get_vertex_array_object(
            program=self.program.programs['skybox'],
            vert_buf_obj = self.vert_buf_obj.vert_buf_objs['skybox']
        )
        
        # advanced skybox vertex array object
        self.vert_arr_objs['advanced_skybox'] = self.get_vertex_array_object(
            program=self.program.programs['advanced_skybox'],
            vert_buf_obj = self.vert_buf_obj.vert_buf_objs['advanced_skybox']
        )

    def get_vertex_array_object(self, program, vert_buf_obj):
        vert_arr_obj = self.ctx.vertex_array(
            program, [(vert_buf_obj.vert_buf_obj, 
                       vert_buf_obj.format, 
                       *vert_buf_obj.attribs)], 
            skip_errors=True
        )
        return vert_arr_obj

    def destroy(self):
        self.vert_buf_obj.destroy()
        self.program.destroy()