#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from setuptools import setup, find_packages

with open(os.path.join('metatoolkit', '__init__.py'), 'r', encoding='utf-8') as f:
    version = re.search(r"__version__\s*=\s*'([\d.]+)'", f.read()).group(1)

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='metatoolkit',
    version=version,
    description='A powerful Python library for processing metadata of images, videos, and audio files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Hmily',
    author_email='',
    url='https://github.com/ihmily/metatoolkit',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='image, metadata, exif, watermark, video, audio',
    python_requires='>=3.10',
    install_requires=[
        'Pillow>=9.5.0',
        'pyexiv2>=2.15.4',
    ],
    entry_points={
        'console_scripts': [
            'metatoolkit=metatoolkit.cli:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/ihmily/metatoolkit/issues',
        'Source': 'https://github.com/ihmily/metatoolkit',
    },
)