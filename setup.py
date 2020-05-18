#!/usr/bin/env python
#
# Copyright 2012 Canonical Ltd.  This software is licensed under the
# GNU General Public License version 3 (see the file LICENSE).

from setuptools import setup

setup(
    name='charm-config',
    version='1.0.0',
    packages=['charm_config'],
    install_requires=[
        'pyyaml',
    ],
    include_package_data=True,
    maintainer='Cory Johns',
    maintainer_email='johnsca@gmail.com',
    description='Plugin for charm snap to view config from the charm store',
    license='GPL v3',
    url='https://github.com/johnsca/charm-config',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
    ],
    entry_points={
        'console_scripts': [
            'charm-config = charm_config:Config.main',
        ],
    },
)
