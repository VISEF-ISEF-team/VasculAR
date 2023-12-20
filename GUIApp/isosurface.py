import vedo
from vedo.plotter import Plotter
from vedo.utils import precision
import SimpleITK as sitk
import numpy as np
from vedo import *

class IsosurfaceBrowser(Plotter):

    def __init__(
        self,
        volume,
        isovalue=None,
        c=None,
        alpha=1,
        lego=False,
        res=50,
        use_gpu=False,
        precompute=False,
        progress=False,
        cmap="hot",
        delayed=False,
        sliderpos=4,
        pos=(0, 0),
        size="auto",
        screensize="auto",
        title="",
        bg="white",
        bg2=None,
        axes=1,
        interactive=True,
    ):
        """
        Generate a `vedo.Plotter` for Volume isosurfacing using a slider.

        Set `delayed=True` to delay slider update on mouse release.

        Set `res` to set the resolution, e.g. the number of desired isosurfaces to be
        generated on the fly.

        Set `precompute=True` to precompute the isosurfaces (so slider browsing will be smoother).

        Examples:
            - [app_isobrowser.py](https://github.com/marcomusy/vedo/tree/master/examples/volumetric/app_isobrowser.py)

                ![](https://vedo.embl.es/images/advanced/app_isobrowser.gif)
        """

        Plotter.__init__(
            self,
            pos=pos,
            bg=bg,
            bg2=bg2,
            size=size,
            screensize=screensize,
            title=title,
            interactive=interactive,
            axes=axes,
        )

        ### GPU ################################
        if use_gpu and hasattr(volume.GetProperty(), "GetIsoSurfaceValues"):

            scrange = volume.scalar_range()
            delta = scrange[1] - scrange[0]
            if not delta:
                return

            if isovalue is None:
                isovalue = delta / 3.0 + scrange[0]

            ### isovalue slider callback
            def slider_isovalue(widget, event):
                value = widget.GetRepresentation().GetValue()
                isovals.SetValue(0, value)

            isovals = volume.GetProperty().GetIsoSurfaceValues()
            isovals.SetValue(0, isovalue)
            self.renderer.AddActor(volume.mode(5).alpha(alpha).c(c))

            self.add_slider(
                slider_isovalue,
                scrange[0] + 0.02 * delta,
                scrange[1] - 0.02 * delta,
                value=isovalue,
                pos=sliderpos,
                title="scalar value",
                show_value=True,
                delayed=delayed,
            )

        ### CPU ################################
        else:

            self._prev_value = 1e30

            scrange = volume.scalar_range()
            delta = scrange[1] - scrange[0]
            if not delta:
                return

            if lego:
                res = int(res / 2)  # because lego is much slower
                slidertitle = ""
            else:
                slidertitle = "scalar value"

            allowed_vals = np.linspace(scrange[0], scrange[1], num=res)

            bacts = {}  # cache the meshes so we dont need to recompute
            if precompute:
                delayed = False  # no need to delay the slider in this case
                if progress:
                    pb = vedo.ProgressBar(0, len(allowed_vals), delay=1)

                for value in allowed_vals:
                    value_name = precision(value, 2)
                    if lego:
                        mesh = volume.legosurface(vmin=value)
                        if mesh.ncells:
                            mesh.cmap(cmap, vmin=scrange[0], vmax=scrange[1], on="cells")
                    else:
                        mesh = volume.isosurface(value).color(c).alpha(alpha)
                    bacts.update({value_name: mesh})  # store it
                    if progress:
                        pb.print("isosurfacing volume..")

            ### isovalue slider callback
            def slider_isovalue(widget, event):

                prevact = self.actors[0]
                if isinstance(widget, float):
                    value = widget
                else:
                    value = widget.GetRepresentation().GetValue()

                # snap to the closest
                idx = (np.abs(allowed_vals - value)).argmin()
                value = allowed_vals[idx]

                if abs(value - self._prev_value) / delta < 0.001:
                    return
                self._prev_value = value

                value_name = precision(value, 2)
                if value_name in bacts:  # reusing the already existing mesh
                    # print('reusing')
                    mesh = bacts[value_name]
                else:  # else generate it
                    # print('generating', value)
                    if lego:
                        mesh = volume.legosurface(vmin=value)
                        if mesh.ncells:
                            mesh.cmap(cmap, vmin=scrange[0], vmax=scrange[1], on="cells")
                    else:
                        mesh = volume.isosurface(value).color(c).alpha(alpha)
                    bacts.update({value_name: mesh})  # store it

                self.renderer.RemoveActor(prevact)
                self.renderer.AddActor(mesh)
                self.actors[0] = mesh

            ################################################

            if isovalue is None:
                isovalue = delta / 3.0 + scrange[0]

            self.actors = [None]
            slider_isovalue(isovalue, "")  # init call
            if lego:
                self.actors[0].add_scalarbar(pos=(0.8, 0.12))

            self.add_slider(
                slider_isovalue,
                scrange[0] + 0.02 * delta,
                scrange[1] - 0.02 * delta,
                value=isovalue,
                pos=sliderpos,
                title=slidertitle,
                show_value=True,
                delayed=delayed,
            )


            
class IsoSurface():
    def __init__(self, volume_image):
        self.volume_image = volume_image
        
    def visualization(self):
        volume = vedo.Volume(self.volume_image) 
        plt = Plotter(N=2)
        
        scrange = volume.scalar_range()
        delta = scrange[1] - scrange[0]
        if not delta:
            return

        isovalue = None
        if isovalue is None:
            isovalue = delta / 3.0 + scrange[0]

        ### isovalue slider callback
        def slider_isovalue(widget, event):
            value = widget.GetRepresentation().GetValue()
            isovals.SetValue(0, value)

        isovals = volume.GetProperty().GetIsoSurfaceValues()
        isovals.SetValue(0, isovalue)
        plt.at(0).renderer.AddActor(volume.mode(5).alpha(1).c('copper'))

        plt.at(0).add_slider(
            slider_isovalue,
            scrange[0] + 0.02 * delta,
            scrange[1] - 0.02 * delta,
            value=isovalue,
            pos=4,
            title="scalar value",
            show_value=True,
            delayed=False,
        )
        
        # plt = IsosurfaceBrowser(vol, use_gpu=True, c='copper')
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

        # Show volume in the first view
        plt.at(0).show(volume)

        # Show text in the second view
        plt.at(1).show(self.txt, axes=0, bg='black')

        # Display the plotter interactively
        plt.interactive()

        # Close the interactive window
        plt.close()


nifti_image = sitk.ReadImage('D:/Documents/GitHub/VascuIAR/DeepLearning/data/MM_WHS/train_images/ct_train_1017_image.nii.gz')
array = sitk.GetArrayFromImage(nifti_image)

instance = IsoSurface(array)
instance.visualization()

