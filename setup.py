#!/usr/bin/env python
"""
django-pigman
=============

Pigman is a Django app that simplifies the integration of the Python Gearman
library into your project.

PYthon Gearman -> pygman -> pigman.
"""


from setuptools import setup, find_packages

import os
import subprocess


# If setup.py is being run from within the git repository (instead of a
# tarball, for instance) append the first 10 digits of the head commmit.
pigman_version = "0.0.1"
if os.path.exists(".git"):
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"])
    pigman_version += "({0})".format(commit[:10])


install_requires = [
    'gearman>=2.0.2,<2.1',
]

setup(
    name='django-pigman',
    version=pigman_version,
    author='Mapkin',
    author_email='dev@mapkin.co',
    url='https://github.com/Mapkin/django-pigman.git',
    description='A Gearman application for Django',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Indended Audience :: Developers',
        'Operating System :: Unix',
        'Topic :: Software Development'
    ],
)
