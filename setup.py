#!/usr/bin/env python

import sys

from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of kdl requires Python {}.{}, but you're trying to
install it on Python {}.{}.
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

setup(name='kdlc',
      version='0.1',
      python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
      description='KNIME DSL Compiler',
      author='KNIME-DSL',
      author_email='KNIME.DSL@gmail.com',
      url='https://github.com/knime-dsl/kdl/',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['kdlc=kdlc.application:main'],
      },
      install_requires=['jinja2', 'pytest', 'coverage'],
      package_data={'kdlc': ['templates/*.xml']},
      include_package_data=True,
     )
