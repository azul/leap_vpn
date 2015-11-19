# -*- coding: utf-8 -*-
# setup.py
# Copyright (C) 2015 LEAP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
Setup file for leap.vpn
"""
from setuptools import setup
from setuptools import find_packages

from pkg import utils

VERSION = "0.1.0"
VERSION_FULL = VERSION_SHORT = VERSION
DOWNLOAD_BASE = 'https://github.com/leapcode/leap_vpn/archive/%s.tar.gz'
DOWNLOAD_URL = DOWNLOAD_BASE % VERSION_SHORT


trove_classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Topic :: Internet',
    'Topic :: Security :: Cryptography',
    'Topic :: Software Development :: Libraries',
]

setup(
    name='leap.vpn',
    version=VERSION,
    url='https://leap.se/',
    download_url=DOWNLOAD_URL,
    license='GPLv3+',
    description="LEAP's VPN Manager",
    author='The LEAP Encryption Access Project',
    author_email='info@leap.se',
    maintainer='Ivan Alejandro',
    maintainer_email='ivanalejandro0@leap.se',
    long_description=(
        "LEAP VPN library."
    ),
    classifiers=trove_classifiers,
    namespace_packages=["leap"],
    packages=find_packages('src', exclude=['leap.vpn.tests']),
    package_dir={'': 'src'},
    test_suite='leap.vpn.tests',
    install_requires=utils.parse_requirements(),
    tests_require=utils.parse_requirements(
        reqfiles=['pkg/requirements-testing.pip']),
)
