from setuptools import Extension, setup
from Cython.Build import cythonize

extensions = [
    Extension(
        name="registrar_core",
        sources=["registrar_core.pyx"],
    )
]

setup(
    name="registrarY-cython-core",
    version="1.0.0",
    description="Cython helpers for registrarY",
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"},
    ),
    zip_safe=False,
)
