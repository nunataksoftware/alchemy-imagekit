#/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
from setuptools import setup, find_packages
import sys


# Workaround for multiprocessing/nose issue. See http://bugs.python.org/msg170215
try:
    import multiprocessing
except ImportError:
    pass


if 'publish' in sys.argv:
    os.system('python setup.py sdist upload')
    sys.exit()


read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

def exec_file(filepath, globalz=None, localz=None):
        exec(read(filepath), globalz, localz)

# Load package meta from the pkgmeta module without loading imagekit.
pkgmeta = {}
exec_file(os.path.join(os.path.dirname(__file__),
         'alchemy-imagekit', 'pkgmeta.py'), pkgmeta)


setup(
    name='alchemy-imagekit',
    version=pkgmeta['__version__'],
    description='Automated image processing for SQLAlchemy models.',
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.rst')),
    author='Guillermo Nuñez',
    author_email='gui.nunez@gmail.com',
    maintainer='Guillermo Nuñez',
    maintainer_email='gui.nunez@gmail.com',
    license='MIT',
    url='https://github.com/nunataksoftware/alchemy-imagekit',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    tests_require=[
        'beautifulsoup4==4.1.3',
        'nose==1.3.0',
        'nose-progressive==1.5',
        'Pillow<3.0',
    ],
    test_suite='testrunner.run_tests',
    install_requires=[
        'pilkit>=1.1.6',
        'six',
    ],
    extras_require={
    },
    keywords = ['image', 'processing', 'sqlalchemy'],
    classifiers = [],

)