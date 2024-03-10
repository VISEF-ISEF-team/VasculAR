from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("_marching_cubes_lorensen_cy.pyx")
)
