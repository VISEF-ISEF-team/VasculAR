from setuptools import setup
from Cython.Build import cythonize
import numpy as np

setup(
    ext_modules=cythonize("_marching_cubes_lorensen_cy.pyx"),
    include_dirs=[np.get_include()]
)
