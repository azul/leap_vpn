# -*- coding: utf-8 -*-
# util.py
# Copyright (C) 2013 LEAP
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
Common configs
"""
import errno
import os

# from dirspec.basedir import get_xdg_config_home


def get_path_prefix(standalone=False):
    """
    Returns the platform dependent path prefix.

    :param standalone: if True it will return the prefix for a standalone
                       application.
                       Otherwise, it will return the system default for
                       configuration storage.
    :type standalone: bool
    """
    return os.path.expanduser("~/.config")  # hardcoded Linux XDG config path

    # TODO: this is to use XDG specifications
    # commented temporarily to avoid that extra dependency

    # config_home = get_xdg_config_home()
    # if standalone:
    #     config_home = os.path.join(os.getcwd(), "config")
    #
    # return config_home


def force_eval(items):
    """
    Return a sequence that evaluates any callable in the sequence,
    instantiating it beforehand if the item is a class, and
    leaves the non-callable items without change.
    """
    def do_eval(thing):
        if isinstance(thing, type):
            return thing()()
        if callable(thing):
            return thing()
        return thing

    if isinstance(items, (list, tuple)):
        return map(do_eval, items)
    else:
        return do_eval(items)


def first(things):
    """
    Return the head of a collection.

    :param things: a sequence to extract the head from.
    :type things: sequence
    :return: object, or None
    """
    try:
        return things[0]
    except (IndexError, TypeError):
        return None


def mkdir_p(path):
    """
    Creates the path and all the intermediate directories that don't
    exist

    Might raise OSError

    :param path: path to create
    :type path: str
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


# Twisted implementation of which
def which(name, flags=os.X_OK, path_extension="/usr/sbin:/sbin"):
    """
    Search PATH for executable files with the given name.

    On newer versions of MS-Windows, the PATHEXT environment variable will be
    set to the list of file extensions for files considered executable. This
    will normally include things like ".EXE". This fuction will also find files
    with the given name ending with any of these extensions.

    On MS-Windows the only flag that has any meaning is os.F_OK. Any other
    flags will be ignored.

    :type name: C{str}
    :param name: The name for which to search.

    :type flags: C{int}
    :param flags: Arguments to L{os.access}.

    :rtype: C{list}
    :param: A list of the full paths to files found, in the
    order in which they were found.
    """

    result = []
    exts = filter(None, os.environ.get('PATHEXT', '').split(os.pathsep))
    path = os.environ.get('PATH', None)
    path = path_extension + os.pathsep + path
    if path is None:
        return []
    parts = path.split(os.pathsep)
    for p in parts:
        p = os.path.join(p, name)
        if os.access(p, flags):
            result.append(p)
        for e in exts:
            pext = p + e
            if os.access(pext, flags):
                result.append(pext)
    return result


def get_vpn_launcher():
    """
    Return the VPN launcher for the current platform.
    """
    from leap.vpn.linuxvpnlauncher import LinuxVPNLauncher
    from leap.vpn.darwinvpnlauncher import DarwinVPNLauncher
    from leap.vpn.windowsvpnlauncher import WindowsVPNLauncher
    from leap.vpn.constants import IS_LINUX, IS_MAC, IS_WIN
    if not (IS_LINUX or IS_MAC or IS_WIN):
        error_msg = "VPN Launcher not implemented for this platform."
        raise NotImplementedError(error_msg)

    launcher = None
    if IS_LINUX:
        launcher = LinuxVPNLauncher
    elif IS_MAC:
        launcher = DarwinVPNLauncher
    elif IS_WIN:
        launcher = WindowsVPNLauncher

    # leap_assert(launcher is not None)
    # XXX fix this
    if launcher is None:
        raise Exception("Launcher is None")

    return launcher()
