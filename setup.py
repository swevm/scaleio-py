#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages
from distutils.core import setup

setup(
    author='Matt Cowger & Magnus Nilson',
    author_email='magnus@karabas.nu,matt@cowger.us',
    name='ScaleIO-py',
    description='Python interface to ScaleIO 1.3 REST API',
    version="0.31",
    url='https://github.com/swevm/scaleio-py/',
    license='Apache License',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        open("requirements.txt").readlines(),
    ],
)