import vedo
from vedo import *

class NewWindow():
    def __init__(self, mesh):
        self.mesh = mesh
        self.current_style = 0
        self.styles = ['default', 'metallic', 'plastic', 'shiny', 'glossy', 'ambient', 'off']
        self.button_styles = []
        self.button_style_state = [0,0,0,0,0,0,0]
    
        
        self.cutting()
        self.slider()
        self.lighting()
        self.analysis()
        self.show()
        
        
    def cutting(self):
        vedo.settings.use_parallel_projection = True
        self.plotter = vedo.applications.FreeHandCutPlotter(self.mesh)
        
    def slider(self):
        def slider1(widget, event):
            self.mesh.color(widget.value)

        def slider2(widget, event):
            self.mesh.alpha(widget.value)    
        
        self.plotter.add_slider(
            slider1,
            xmin=-9,
            xmax=1,
            value=0,
            pos="bottom-right",
            title="color number",
        )
        self.plotter.add_slider(
            slider2,
            xmin=0.01,
            xmax=1,
            value=0.5,
            c="blue",
            pos="bottom-right-vertical",
            title="alpha value (opacity)",
        )
        
    def lighting(self):
        def change_style(index):
            def buttonfunc():
                self.button_style_state[index] = 1 - self.button_style_state[index]
                self.button_styles[index].switch()  
                if self.button_style_state[index] == 1:
                    self.mesh.lighting(self.styles[index])     
                else:
                    self.mesh.lighting(self.styles[0])
            return buttonfunc
        
        for index in range(len(self.styles)):
            button = self.plotter.add_button(
                change_style(index),
                pos=(0.03, 0.24 - index * 0.03),
                states=["off", "on"],
                c=["w", "w"],
                bc=["#0d6efd", "dv"],
                font="courier",
                size=10,
                bold=True,
                italic=False,
                angle=0.3,
            )
            
            self.button_styles.append(button)

    def analysis(self):
        # Create a paragraph of text
        text_content = """
        ********************************************
        Đoạn chẩn đoán gợi ý bệnh lý dưới đây 
        được tạo ra từ mô hình Deep Learning
        của VasculAR, cần được duyệt qua bởi 
        người có chuyên môn. Bạn có thể chỉnh
        sửa nội dung bằng phần mềm VasculAR.
        
        ********************************************
        
        Đây là nội dung phân tích:
        """

        # Create a Text object with the specified content
        self.txt = Text2D(text_content, pos=('top-left'), font='C:/Windows/Fonts/Arial.ttf', s=0.7, c='w')
        

    def show(self):
        show(self.mesh, self.txt, at=0, bg='black', interactive=True)
        self.plotter.add_hover_legend()
        self.plotter.start(axes=1, bg='black').close()

mesh = load("D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/SegmentationData/ct_0022_label_resized/label_6_myocardium.stl")
mesh.color("white")
mesh.smooth(niter=100).lighting('default')
mesh.texture('textures/cardiac_texture_3.jpg')
instance = NewWindow(mesh)
