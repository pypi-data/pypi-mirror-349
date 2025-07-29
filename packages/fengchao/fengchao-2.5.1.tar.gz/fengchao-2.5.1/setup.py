# -*- coding:utf-8 -*-
"""
# File       : setup.py
# Time       ：2024/2/23 16:50
# Author     ：andy
# version    ：python 3.9
"""
import io
# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import os
import sys
import time
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'fengchao'
DESCRIPTION = '大模型框架服务调用SDK.'
URL = ''
EMAIL = ''
AUTHOR = 'ijiwei'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    'requests==2.31.0', 'pyJWT==2.8.0', 'pydantic==2.6.1', 'tenacity==8.2.3', 'loguru'
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'fengchao','README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass
    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('deleted build')
        os.system('rm -rf build/')

        self.status('deleted dist')
        os.system('rm -rf dist/')

        self.status('deleted fengchao.egg-info')
        os.system('rm -rf fengchao.egg-info/')

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('/aigc/miniconda3/envs/ijiwei_aigc/bin/twine upload dist/* --verbose')
        # token pypi-AgEIcHlwaS5vcmcCJDE0MTViNmIzLWUwYWQtNDViNS05MGRmLTlhZDhhNzFjZWUxZAACKlszLCI5MjZkMDVkZS05MmRkLTQzNTEtYTRjZS0xMGU1Mzk5YTEwMmQiXQAABiCUWlxzM8tcR5wMgZUdKFd3cEmvdLOsZOwdtZTTmk28EA

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["test", "configs", "core"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['fengchao'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)