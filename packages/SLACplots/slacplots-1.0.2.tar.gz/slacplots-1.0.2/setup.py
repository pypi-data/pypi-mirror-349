#!/usr/bin/env python

import setuptools

VER = "1.0.2"

reqs = ["matplotlib",
        ]

setuptools.setup(
    name="SLACplots",
    version=VER,
    author="Daniel Douglas",
    author_email="dougl215@slac.stanford.edu",
    description="Plotting utilities for matplotlib in the SLAC style",
    url="https://github.com/DanielMDouglas/SLACplots",
    packages=setuptools.find_packages(),
    install_requires=reqs,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    python_requires='>=3.2',
)
