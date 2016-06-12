"""
Py Db Report
--------

A small report system for python

"""
from setuptools import setup, find_packages
requirements = open('requirements.txt').read().split('\n')
setup(
    name='Vaca',
    version='0.0',
    url='https://github.com/carrerasrodrigo/vaca',
    license='bsd',
    author='Rodrigo N. Carreras',
    author_email='carrerasrodrigo@gmail.com',
    description='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[],
    install_requires=requirements,
    entry_points={
        'console_scripts': ['vaca=vaca.terminal:start'],
    },
)
