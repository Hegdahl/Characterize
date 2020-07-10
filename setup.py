'''Installation script run by pip'''
from setuptools import setup, find_packages

setup(
    name='characterize',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'pillow',
    ],
    description='Tool for creating console printable images using ANSI escapes.',
    project_urls={
        'Source Code': 'https://github.com/Hegdahl/pyclichess',
    },
    classifiers=[
        'License :: MIT :: Copyright (c) 2019 Magnus Hegdahl'
    ],
    entry_points={
        'console_scripts': [
            'characterize = characterize:main',
        ],
    }
)
