# -*- coding: utf-8 -*-
# logs.py
# Copyright (C) 2013, 2014, 2015 LEAP
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
Logs utilities
"""

import os
import sys

# from leap.bitmask.util import get_path_prefix
from leap.vpn.utils import get_path_prefix
# from leap.common.files import mkdir_p
from leap.vpn.utils import mkdir_p

import logbook
from logbook.more import ColorizedStderrHandler

LOG_FORMAT = (u'[{record.time:%Y-%m-%d %H:%M:%S}] '
              u'{record.level_name: <8} - L#{record.lineno: <4} : '
              u'{record.module}:{record.func_name} - {record.message}')


def get_logger(perform_rollover=False):
    """
    Push to the app stack the needed handlers and return a Logger object.

    :rtype: logbook.Logger
    """
    # NOTE: make sure that the folder exists, the logger is created before
    # saving settings on the first run.
    _base = os.path.join(get_path_prefix(), "leap")
    mkdir_p(_base)
    bitmask_log_file = os.path.join(_base, 'bitmask.log')

    # level = logbook.WARNING
    # if flags.DEBUG:
    #     level = logbook.NOTSET
    level = logbook.NOTSET

    # This handler consumes logs not handled by the others
    null_handler = logbook.NullHandler()
    null_handler.push_application()

    file_handler = logbook.RotatingFileHandler(
        bitmask_log_file, format_string=LOG_FORMAT, bubble=True,
        max_size=sys.maxint)

    if perform_rollover:
        file_handler.perform_rollover()

    file_handler.push_application()

    stream_handler = ColorizedStderrHandler(
        level=level, format_string=LOG_FORMAT, bubble=True)
    stream_handler.push_application()

    logger = logbook.Logger('leap')

    return logger
