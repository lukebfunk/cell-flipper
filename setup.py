"""Adapted from https://github.com/pypa/sampleproject
"""

from setuptools import setup
# from os import path

# here = path.abspath(path.dirname(__file__))

setup(
    name='cell-flipper',
    version='0.1',
    description='GUI for quickly classifying labeled images',  # Required
    # long_description=long_description,
    url='http://github.com/lukebfunk/cell-flipper',
    author='lukebfunk',  # Optional
    author_email='lukefunk@broadinstitute.org',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=['cell-flipper'],
)
