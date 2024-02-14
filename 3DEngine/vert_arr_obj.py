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
            vbo = self.vert_buf_obj.vbos['cube']
        )

    def get_vertex_array_object(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True)
        return vao

    def destroy(self):
        self.vert_buf_obj.destroy()
        self.program.destroy()