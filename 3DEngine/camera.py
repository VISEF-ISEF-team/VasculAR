import glm

FOV = 50
NEAR = 0.1
FAR = 100

class Camera:
    def __init__ (self, app):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(2, 3, 3)
        self.up = glm.vec3(0, 1, 0)
        self.matrix_view = self.get_view_matrix() 
        self.matrix_projection = self.get_projection_matrix()
        
    def get_projection_matrix(self):
        return glm.perspective(
            glm.radians(FOV),
            self.aspect_ratio,
            NEAR, FAR
        )
    
    def get_view_matrix(self):
        return glm.lookAt(self.position, glm.vec3(0), self.up)