from vedo import *
import vedo
from screeninfo import get_monitors
import os

class SplinePlotter(Plotter):
    """
    Interactive drawing of splined curves on meshes.
    """

    def __init__(self, obj, init_points=(), closed=False, splined=True, **kwargs):
        """
        Create an interactive application that allows the user to click points and
        retrieve the coordinates of such points and optionally a spline or line
        (open or closed).

        Input object can be a image file name or a 3D mesh.
        """
        super().__init__(**kwargs)

        self.mode = "trackball"
        self.verbose = True
        self.splined = splined
        self.resolution = None  # spline resolution (None = automatic)
        self.closed = closed
        self.lcolor = "yellow4"
        self.lwidth = 3
        self.pcolor = "purple5"
        self.psize = 10

        self.cpoints = list(init_points)
        self.vpoints = None
        self.line = None

        if isinstance(obj, str):
            self.object = vedo.file_io.load(obj)
        else:
            self.object = obj

        if isinstance(self.object, vedo.Picture):
            self.mode = "image"
            self.parallel_projection(True)

        t = (
            "Chuột trái để khoanh vùng\n"
            "Chuột phải để xóa đi\n"
            "Kéo chuột để thay đổi độ tương phản\n"
            "Chọn c để xóa khoanh vùng\n"
            "Chọn q để hủy bỏ"
        )
        self.instructions = Text2D(t, pos="bottom-left", c="white", s=0.5, font="C:/Windows/Fonts/Arial.ttf")

        self += [self.object, self.instructions]

        self.callid1 = self.add_callback("KeyPress", self._key_press)
        self.callid2 = self.add_callback("LeftButtonPress", self._on_left_click)
        self.callid3 = self.add_callback("RightButtonPress", self._on_right_click)

    def points(self, newpts=None):
        """Retrieve the 3D coordinates of the clicked points"""
        if newpts is not None:
            self.cpoints = newpts
            self._update()
            return self
        return np.array(self.cpoints)

    def _on_left_click(self, evt):
        if not evt.actor:
            return
        if evt.actor.name == "points":
            # remove clicked point if clicked twice
            pid = self.vpoints.closest_point(evt.picked3d, return_point_id=True)
            self.cpoints.pop(pid)
            self._update()
            return
        p = evt.picked3d
        self.cpoints.append(p)
        self._update()
        if self.verbose:
            vedo.colors.printc("Added point:", precision(p, 4), c="g")

    def _on_right_click(self, evt):
        if evt.actor and len(self.cpoints) > 0:
            self.cpoints.pop()  # pop removes from the list the last pt
            self._update()
            if self.verbose:
                vedo.colors.printc("Deleted last point", c="r")

    def _update(self):
        self.remove(self.line, self.vpoints)  # remove old points and spline
        self.vpoints = Points(self.cpoints).ps(self.psize).c(self.pcolor)
        self.vpoints.name = "points"
        self.vpoints.pickable(True)  # to allow toggle
        minnr = 1
        if self.splined:
            minnr = 2
        if self.lwidth and len(self.cpoints) > minnr:
            if self.splined:
                try:
                    self.line = Spline(self.cpoints, closed=self.closed, res=self.resolution)
                except ValueError:
                    # if clicking too close splining might fail
                    self.cpoints.pop()
                    return
            else:
                self.line = Line(self.cpoints, closed=self.closed)
            self.line.c(self.lcolor).lw(self.lwidth).pickable(False)
            self.add(self.vpoints, self.line)
        else:
            self.add(self.vpoints)

    def _key_press(self, evt):
        if evt.keypress == "c":
            self.cpoints = []
            self.remove(self.line, self.vpoints).render()
            if self.verbose:
                vedo.colors.printc("==== Cleared all points ====", c="r", invert=True)

    def start(self):
        """Start the interaction"""
        self.show(self.object, self.instructions, mode=self.mode)
        return self


class BoundingImage():
    def __init__(self, picture):
        self.picture = picture
        self.screens = get_monitors()
        self.plt = SplinePlotter(self.picture, size=(600, 600), pos=(int(self.screens[0].width/3), int(self.screens[0].height/3)))
        self.par_dir =  os.path.dirname(self.picture)
        self.screenshot_func()
        self.plt.show(mode="image", bg='black', zoom='tightest')
        
    def screenshot_func(self):    
        def screenshot(evt=None):
            self.plt.screenshot(os.path.join(self.par_dir, f'{os.path.basename(self.picture)}_screenshot.png'))

        screenshot_btn = self.plt.add_button(    
            screenshot,
            pos=(0.5, 0.9),                                                                   
            states=['Lưu ảnh khoanh vùng', 'Lưu ảnh khoanh vùng'],                    
            c=["w", "w"],                                                                 
            bc=["#0d6efd", "dv"],                                                                         
            font='C:/Windows/Fonts/Arial.ttf',                                 
            size=15,                                                                              
            bold=True,                                                                             
            italic=False,                                                                          
            angle=0.3,        
        )
        

isinstance = BoundingImage(
    picture="D:/Documents/GitHub/VascuIAR/DeepLearning/3D_reconstruction/textures/cardiac_texture_5.png",
)