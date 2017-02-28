#!/usr/bin/env python

from setuptools import setup, find_packages

exec(compile(open('version.py').read(), 'version.py', 'exec'))

setup(name='sunnydi',
      version=__version__,
      description='SunnyDI dependency injection framework',
      author='Justin Smith',
      author_email='justin@thomasstreet.com',
      maintainer='Justin Smith',
      maintainer_email='justin@thomasstreet.com',
      url='https://www.sunnydi.com/',
      packages=find_packages(exclude=['test', 'docs']),
      package_data={
            'sunnydi': ['../version.py', '../LICENSE'],
      },
      include_package_data=True,
      install_requires=[
          "Flask>=0.10.1"
      ]
      )
