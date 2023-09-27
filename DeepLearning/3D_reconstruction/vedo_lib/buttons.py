from vedo import *

# Define a function that toggles the transparency of a mesh and changes the button state
def buttonfunc1():
    mesh1.alpha(1 - mesh1.alpha())  
    bu1.switch()                   

def buttonfunc2():
    mesh2.alpha(1 - mesh2.alpha())  
    bu2.switch()
    
def buttonfunc3():
    mesh3.alpha(1 - mesh3.alpha())  
    bu3.switch()

def buttonfunc4():
    mesh4.alpha(1 - mesh4.alpha())  
    bu4.switch()

def buttonfunc5():
    mesh5.alpha(1 - mesh5.alpha())  
    bu5.switch()
    
def buttonfunc6():
    mesh6.alpha(1 - mesh6.alpha())  
    bu6.switch()
    
def buttonfunc7():
    mesh7.alpha(1 - mesh7.alpha())  
    bu7.switch()
    
# Load a mesh and set its color to violet
mesh1 = load("../res_recon_full_seg/cardiac_class_1.stl").color('red').smooth(niter=100)
mesh2 = load("../res_recon_full_seg/cardiac_class_2.stl").color('green').smooth(niter=100)
mesh3 = load("../res_recon_full_seg/cardiac_class_3.stl").color('blue').smooth(niter=100)
mesh4 = load("../res_recon_full_seg/cardiac_class_4.stl").color('yellow').smooth(niter=100)
mesh5 = load("../res_recon_full_seg/cardiac_class_5.stl").color('magenta').smooth(niter=100)
mesh6 = load("../res_recon_full_seg/cardiac_class_6.stl").color('cyan').smooth(niter=100)
mesh7 = load("../res_recon_full_seg/cardiac_class_7.stl").color('white').smooth(niter=100)

# Create an instance of the Plotter class with axes style-11 enabled
plt = Plotter()

# Add a button to the plotter with buttonfunc as the callback function
bu1 = plt.add_button(
    buttonfunc1,
    pos=(0.2, 0.05),  # x,y fraction from bottom left corner
    states=["Mesh1 off", "Mesh1 on"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["#0d6efd", "dv"],  # background color for each state
    font="courier",   # font type
    size=10,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style
    angle=0.3,
)

bu2 = plt.add_button(
    buttonfunc2,
    pos=(0.3, 0.05),  # x,y fraction from bottom left corner
    states=["Mesh2 off", "Mesh2 on"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["#0d6efd", "dv"],  # background color for each state
    font="courier",   # font type
    size=10,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style
    angle=0.3,
)


bu3 = plt.add_button(
    buttonfunc3,
    pos=(0.4, 0.05),  # x,y fraction from bottom left corner
    states=["Mesh3 off", "Mesh3 on"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["#0d6efd", "dv"],  # background color for each state
    font="courier",   # font type
    size=10,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style
    angle=0.3,
)


bu4 = plt.add_button(
    buttonfunc4,
    pos=(0.5, 0.05),  # x,y fraction from bottom left corner
    states=["Mesh4 off", "Mesh4 on"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["#0d6efd", "dv"],  # background color for each state
    font="courier",   # font type
    size=10,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style
    angle=0.3,
)


bu5 = plt.add_button(
    buttonfunc5,
    pos=(0.6, 0.05),  # x,y fraction from bottom left corner
    states=["Mesh5 off", "Mesh5 on"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["#0d6efd", "dv"],  # background color for each state
    font="courier",   # font type
    size=10,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style
    angle=0.3,
)


bu6 = plt.add_button(
    buttonfunc6,
    pos=(0.7, 0.05),  # x,y fraction from bottom left corner
    states=["Mesh6 off", "Mesh6 on"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["#0d6efd", "dv"],  # background color for each state
    font="courier",   # font type
    size=10,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style
    angle=0.3,
)

bu7 = plt.add_button(
    buttonfunc7,
    pos=(0.8, 0.05),  # x,y fraction from bottom left corner
    states=["Mesh7 off", "Mesh7 on"],  # text for each state
    c=["w", "w"],     # font color for each state
    bc=["#0d6efd", "dv"],  # background color for each state
    font="courier",   # font type
    size=10,          # font size
    bold=True,        # bold font
    italic=False,     # non-italic font style
    angle=0.3,
)


# Show the mesh, docstring, and button in the plot
plt.show(mesh1, mesh2, mesh3, mesh4, mesh5, mesh6, mesh7, bg='black')