from vedo import *
c1 = Cylinder(pos=(0,0,0), r=2, height=3, axis=(1,.0,0), alpha=.1).triangulate()
c2 = Cylinder(pos=(0,0,2), r=1, height=2, axis=(0,.3,1), alpha=.1).triangulate()

intersect = c1.intersect_with(c2).join(reset=True)
spline = Spline(intersect).c('blue').lw(5)
plt = show(c1, c2, spline, intersect.labels('id'), axes=1)
sptool = plt.add_spline_tool(spline.points(), closed=False)
sptool.AddObserver(
    "end of interaction", 
    lambda o, e: (
        print(f"Spline changed! CM = {sptool.spline().center_of_mass()}"),
        print(f"\tNumber of points: {sptool.spline().vertices.size}"),
    )
)
plt.interactive()
sptool.off()
modified_spline = sptool.spline().c('red').lw(5)
show(modified_spline, interactive=True, resetcam=False).close()