#!/usr/bin/env python
import os
from typing import List
from setuptools import setup, find_packages


def readme() -> str:
    """
    Read README.md.
    :returns: The README contents of the project.
    """
    with open('README.md') as file:
        return file.read()


def read_requirements(filename='requirements.txt') -> List[str]:
    """
    Read the passed requirements file into multiple lines.
    :returns: The requirements list.
    """
    with open(filename) as file:
        lines = [line for line in file.read().splitlines()
                 if not line.startswith('--extra-index-url')]
        return lines


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read().strip()


def get_version(filename='VERSION'):
    # reads the version from the file given
    try:
        version = read(filename)
    except Exception as e:
        print("If you are installing from a branch please run 'make install'.")
        raise e
    return version


setup(
    name="mab",
    description="""MAB Library""",
    long_description=readme(),
    author="Bruno Vaz",
    author_email="bgvaz@corporativo.pt",
    packages=find_packages(
        where="./mab",
        exclude=[]
    ),
    install_requires=read_requirements(),
    version=get_version(),
    include_package_data=True,
)
