from setuptools import setup, find_packages

import os, sys

print("setup.py: BUILD_TOKEN =", os.environ.get("BUILD_TOKEN"), file=sys.stderr)


setup(
    name='goat-pypi-project',
    version='0.1.0',
    author='Daniel Nebenzahl',
    author_email='dn@scribesecurity.com',
    description='A Python package for goat-related functionalities',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/goat-pypi-project',
    packages=find_packages(),
    # classifiers=[
    #     'Programming Language :: Python :: 3',
    #     'Operating System :: OS Independent',
    # ],
    python_requires='>=3.6',
    install_requires=[
        # Add your package dependencies here
    ],
)