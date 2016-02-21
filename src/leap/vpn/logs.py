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

import logging
import os
import sys

# from leap.common.files import mkdir_p
from leap.vpn.utils import mkdir_p
from leap.vpn.constants import IS_WIN

# levelname length == 8, since 'CRITICAL' is the longest
LOG_FORMAT = ('%(asctime)s - %(levelname)-8s - '
              'L#%(lineno)-4s : %(name)s:%(funcName)s() - %(message)s')


def get_logger(debug=True, logfile=None, replace_stdout=False):
    """
    Create the logger and attach the handlers.

    :param debug: the level of the messages that we should log
    :type debug: bool
    :param logfile: the file name of where we should to save the logs
    :type logfile: str
    :param replace_stdout: wether we should pipe all stdout/stderr to the
                           logger or not
    :type replace_stdout: bool

    :return: the new logger with the attached handlers.
    :rtype: logging.Logger
    """
    # TODO: get severity from command line args
    if debug:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    # Create logger and formatter
    logger = logging.getLogger(name='leap.vpn')
    logger.setLevel(level)
    formatter = logging.Formatter(LOG_FORMAT)

    # Console handler
    try:
        import coloredlogs
        coloredlogs.install(level='DEBUG')
    except ImportError:
        console = logging.StreamHandler()
        console.setLevel(level)
        console.setFormatter(formatter)
        using_coloredlog = False
    else:
        using_coloredlog = True

    if using_coloredlog:
        replace_stdout = False

    # File handler
    if logfile is not None:
        base_path = os.path.dirname(logfile)
        mkdir_p(base_path)
        logger.debug('Setting logfile to %s ', logfile)
        fileh = logging.FileHandler(logfile)
        fileh.setLevel(logging.DEBUG)
        fileh.setFormatter(formatter)
        logger.addHandler(fileh)
        logger.debug('File handler plugged!')

    if replace_stdout:
        replace_stdout_stderr_with_logging(logger)

    return logger


def replace_stdout_stderr_with_logging(logger):
    """
    Replace:
        - the standard output
        - the standard error
        - the twisted log output
    with a custom one that writes to the logger.
    """
    # Disabling this on windows since it breaks ALL THE THINGS
    # The issue for this is #4149
    if not IS_WIN:
        sys.stdout = StreamToLogger(logger, logging.DEBUG)
        sys.stderr = StreamToLogger(logger, logging.ERROR)

        # Replace twisted's logger to use our custom output.
        from twisted.python import log
        log.startLogging(sys.stdout)


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.

    Credits to:
    http://www.electricmonk.nl/log/2011/08/14/\
        redirect-stdout-and-stderr-to-a-logger-in-python/
    """
    def __init__(self, logger, log_level=logging.INFO):
        """
        Constructor, defines the logger and level to use to log messages.

        :param logger: logger object to log messages.
        :type logger: logging.Handler
        :param log_level: the level to use to log messages through the logger.
        :type log_level: int
                        look at logging-levels in 'logging' docs.
        """
        self._logger = logger
        self._log_level = log_level

    def write(self, data):
        """
        Simulates the 'write' method in a file object.
        It writes the data receibed in buf to the logger 'self._logger'.

        :param data: data to write to the 'file'
        :type data: str
        """
        for line in data.rstrip().splitlines():
            self._logger.log(self._log_level, line.rstrip())

    def flush(self):
        """
        Dummy method. Needed to replace the twisted.log output.
        """
        pass
