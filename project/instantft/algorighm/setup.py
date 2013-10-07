from distutils.core import setup, Extension

setup(name='castar',
      version='1.0',
      ext_modules=[Extension('castar', ['castar.c'])],
      )
