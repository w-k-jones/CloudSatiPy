from setuptools import setup, find_packages

setup(
    name='cloudsatipy',
    version='0.0.1',
    url='https://github.com/w-k-jones/CloudSatiPy.git',
    author='William Jones',
    author_email='william.jones@physics.ox.ac.uk',
    description='Read CloudSat HDF files into xarray datasets',
    packages=find_packages(),    
    install_requires=[],
)