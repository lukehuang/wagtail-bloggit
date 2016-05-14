# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup, find_packages

dependency_links = []


def parse_requirements_file(filename):
    """
    Given a requirements file, returns a list of requirements that setuptools will understand and add dependency links
    to the global list.
    """
    requires = []
    requirements_file = parse_requirements(filename, session=PipSession())
    for req in requirements_file:
        requires.append(str(req.req))
        if req.link and str(req.link) not in dependency_links:
            dependency_links.append(str(req.link))

    return requires

setup(
    name='wagtail-blogging',
    version='0.1',
    description='Blogging extensions for Wagtail',
    author='Pieter De Decker',
    packages=find_packages(),
    zip_safe=False,
    install_requires=parse_requirements_file('requirements.txt'),
)
