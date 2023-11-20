from vedo import *

plt = Plotter(axes=5)

plt += Text3D(__doc__).bc('tomato')

elg = Picture(dataurl+"images/embl_logo.jpg")

plt.add_icon(elg, pos=2, size=0.06)
plt.add_icon(VedoLogo(), pos=1, size=0.06)

plt.show().close()