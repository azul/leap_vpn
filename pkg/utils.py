# -*- coding: utf-8 -*-
# utils.py
# Copyright (C) 2015 LEAP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Utils to help in the setup process
"""
import os
import re
import sys


def get_reqs_from_files(files):
    """
    Return the contents of the specified files as a list of strings.

    :param reqfiles: files to parse
    :type reqfiles: list of str

    :rtype: list of str
    """
    for reqfile in files:
        if os.path.isfile(reqfile):
            return open(reqfile, 'r').read().split('\n')


def parse_requirements(reqfiles=None):
    """
    Parse the requirement files given as parameters or some default ones.

    The passed requirement files is a list of possible locations to try, the
    function will return the contents of the first path found.

    :param reqfiles: requirement files to parse
    :type reqfiles: list of str
    """
    if reqfiles is None:
        reqfiles = ['requirements.txt', 'requirements.pip',
                    'pkg/requirements.txt', 'pkg/requirements.pip']

    requirements = []
    raw_reqs = get_reqs_from_files(reqfiles)
    if raw_reqs is None:
        return

    for line in raw_reqs:
        # -e git://foo.bar/baz/master#egg=foobar
        if re.match(r'\s*-e\s+', line):
            pass
            # do not try to do anything with externals on vcs
            # requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1',
            #                     line))
            # http://foo.bar/baz/foobar/zipball/master#egg=foobar
        elif re.match(r'\s*https?:', line):
            requirements.append(re.sub(r'\s*https?:.*#egg=(.*)$', r'\1',
                                line))
        # -f lines are for index locations, and don't get used here
        elif re.match(r'\s*-f\s+', line):
            pass

        # argparse is part of the standard library starting with 2.7
        # adding it to the requirements list screws distro installs
        elif line == 'argparse' and sys.version_info >= (2, 7):
            pass
        # do not include comments
        elif line.lstrip().startswith('#'):
            pass
        else:
            if line != '':
                requirements.append(line)

    return requirements
