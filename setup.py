#!/usr/bin/env python

import re
import os
import io
from setuptools import setup, find_packages, Command


def get_version():

    # create a dummy file if it doesn't exist
    if not os.path.exists('version.py'):
        with open('version.py', 'w') as f:
            f.write("__version__ = '0.0.0'\n")

    # now open and parse the version number
    with open('version.py') as f:
        contents = f.read()
        version = re.search(r"__version__\s*=\s*'(.*)'", contents, re.M).group(1)
        return version


class GenerateVersionCommand(Command):
    """
    Create a `version.py` file containing the
    specified version information.
    """
    description = 'generate version number file'

    user_options = [
        ('major=', 'm', 'major version number'),
        ('minor=', 'n', 'minor version number'),
        ('revision=', 'r', 'revision number'),
        ('variant=', 'v', 'build variant'),
    ]

    def initialize_options(self):
        self.major = 0
        self.minor = 0
        self.revision = 0
        self.variant = None

    def finalize_options(self):
        pass

    def run(self):
        with open('version.py', 'w') as f:
            if self._variant_defined:
                f.write("__version__ = '%s.%s.%s-%s'\n" % (self.major, self.minor, self.revision, self.variant))
            else:
                f.write("__version__ = '%s.%s.%s'\n" % (self.major, self.minor, self.revision))

    @property
    def _variant_defined(self):
        return self.variant is not None and self.variant != ''


# Get the long description from the README file
cwd = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(cwd, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='sunnydi',
      version=get_version(),
      description='SunnyDI dependency injection framework',
      long_description=long_description,
      author='Justin Smith',
      author_email='justin@thomasstreet.com',
      maintainer='Justin Smith',
      maintainer_email='justin@thomasstreet.com',
      license='MIT',
      url='https://www.thomasstreet.com/',
      packages=find_packages(exclude=['test', 'docs']),
      package_data={
          'sunnydi': ['../version.py', '../LICENSE'],
      },
      include_package_data=True,
      install_requires=[],
      cmdclass={
          'version': GenerateVersionCommand
      },
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
      keywords='sample setuptools development',
      )
