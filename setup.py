#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Jake Cui
# Mail: cqp@cau.edu.cn
# Created Time:  2022-04-24 22:04:41
#############################################

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


requirements = [
    'Bio', 'pandas', 'setuptools', 'cvmblaster'
]


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(
    name="ResBlaster",
    version=get_version("ResBlaster/__init__.py"),
    keywords=["pip", "wgs", "blastn", "amr"],
    description="find antimcirobial resistance genes on genomes",
    long_description="",
    license="MIT Licence",
    url="https://github.com/hbucqp/ResBlaster",
    author="Jake Cui",
    author_email="cqp@cau.edu.cn",
    packages=find_packages(),
    include_package_data=True,
    # package_data={'': ['*']},
    platforms="any",
    install_requires=requirements,
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'ResBlaster=ResBlaster.ResBlaster:main',
        ],
    },
)
