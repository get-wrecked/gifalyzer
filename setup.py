#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import re
from setuptools import setup, find_packages

install_requires = [
    'pillow',
    'requests',
]

version_file = os.path.join(os.path.dirname(__file__), 'gifalyzer', '_version.py')
with open(version_file) as fh:
    version_file_contents = fh.read().strip()
    version_match = re.match(r"__version__ = '(\d+\.\d+.\d+.*)'", version_file_contents)
    version = version_match.group(1)

setup(
    name='gifalyzer',
    version=version,
    author='Tarjei Husøy',
    author_email='git@thusoy.com',
    url='https://github.com/megacool/gifalyzer',
    description="GIF analysis tool",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'gifalyzer = gifalyzer.__main__:main',
        ]
    },
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia :: Graphics',
    ],
)
