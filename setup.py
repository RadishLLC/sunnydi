#!/usr/bin/env python

import os
from setuptools import setup, find_packages, Command


def get_version():

    # create a dummy file if it doesn't exist
    if not os.path.exists('version.py'):
        with open('version.py', 'w') as f:
            f.write("__version__ = '0.0.0'\n")

    # now open and parse the version number
    exec(compile(open('version.py').read(), 'version.py', 'exec'))

    return __version__


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


setup(name='sunnydi',
      version=get_version(),
      description='SunnyDI dependency injection framework',
      author='Justin Smith',
      author_email='justin@thomasstreet.com',
      maintainer='Justin Smith',
      maintainer_email='justin@thomasstreet.com',
      url='https://www.thomasstreet.com/',
      packages=find_packages(exclude=['test', 'docs']),
      package_data={
            'sunnydi': ['../version.py', '../LICENSE'],
      },
      include_package_data=True,
      cmdclass={
          'version': GenerateVersionCommand
      },
      )
