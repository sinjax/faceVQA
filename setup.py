#!/usr/bin/env python

from setuptools import setup

setup(name='faceVQA',
      version='1.0',
      description='Face VQA',
      author='Sina Samangooei, Pouya Samangouei',
      author_email='sinjax@gmail.com',
      packages=['facevqa'],
      install_requires=[
        "keras>=1.1.0",
        "scikit-learn>=0.17.1",
        "PyLD>=0.7.1"
      ]
 )
