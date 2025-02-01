from setuptools import setup
from Cython.Build import cythonize

setup(
    name='extract_objects',
    ext_modules=cythonize("mops/extract_objects.pyx"),
)
