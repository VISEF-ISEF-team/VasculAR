import numpy as np
print(np.version.version)

data = dict()
levels = [0.05, -0.05, 0.0005, -0.0005]
for level in levels:
    data[level] = np.load(f"D:/BlenderBasedProjects/Materials/data_{level}.npz")
    
print(data)
