#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='nertagger',
    description='Nertagger',
    version='1.0.0',
    install_requires=[
        'django',
        'django-debug-toolbar',
        'psycopg2',
        'django-debug-panel'
    ],
    author='Alexander Tkachenko',
    packages=find_packages(),
)
