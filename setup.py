#!/usr/bin/env python
from setuptools import setup, find_packages

__about__ = {}

with open("recliner/__about__.py") as fp:
    exec(fp, None, __about__)

setup(
    name=__about__["__title__"],
    version=__about__["__version__"],

    description=__about__["__summary__"],
    long_description=open("README.rst").read(),
    url=__about__["__uri__"],
    license=__about__["__license__"],

    author=__about__["__author__"],
    author_email=__about__["__email__"],

    install_requires=[
        "bleach>=1.2",
        "docutils>=0.9",
        "Pygments",
    ],
    extras_require={
        "tests": [
            "pep8",
            "pylint",
            "pytest",
            "pytest-cov",
        ],
    },
    tests_require=[
        "pep8",
        "pytest",
        "pytest-cov",
    ],

    packages=find_packages(exclude=["tests"]),

    entry_points={
        "console_scripts": [
            "recliner = recliner.__main__:main",
        ],
    },

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],

    zip_safe=False,
)
