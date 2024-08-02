from setuptools import setup, find_packages

DESCRIPTION = 'This library is a collection of fundamental functionalities for hyperspectral image analysis'
NAME = 'hsitools'
AUTHOR = 'dekkaiinu'
URL = 'https://github.com/dekkaiinu/hsitools'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/dekkaiinu/hsitools'
VERSION = '0.1.60'
PYTHON_REQUIRES = '>=3.8.18'

INSTALL_REQUIRES = [
    'matplotlib>=3.7.5',
    'numpy>=1.24.4',
    'opencv-python>=4.9.0.80'
]

with open('README.md', 'r') as fp:
    readme = fp.read()

setup(name=NAME,
      author=AUTHOR,
      description=DESCRIPTION,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages(),
    )