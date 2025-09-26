"""
Install script -> Just do pip install -e .  (for editing)
"""

from setuptools import setup, find_packages

setup(
    name='cgp',
    version='0.1',
    description=(
        'library of algorithmic implementations'
    ),
    author='William Bowley',
    author_email='wgrantbowley@gmail.com',
    packages=find_packages(include=["primitives"]),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    python_requires='>=3.8',
    include_package_data=True,
)
