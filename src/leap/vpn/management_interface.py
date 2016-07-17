# -*- coding: utf-8 -*-
# vpnprocess.py
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
VPN Management Interface, wrapper for the OpenVPN API.
"""

import socket

from leap.vpn.udstelnet import UDSTelnet
from leap.vpn.logs import get_logger

logger = get_logger()

class ManagementInterface(object):
    """
    This is a thin wrapper around the VPN Management Interface.

    It handles all the low level socket stuff.
    It should be easy to mock in order to test its callers.
    """

    def __init__(self):
        self._tn = None

    def _seek_to_eof(self):
        """
        Read as much as available. Position seek pointer to end of stream
        """
        try:
            self._tn.read_eager()
        except EOFError:
            logger.debug("Could not read from socket. Assuming it died.")
            return

    def _send_command(self, command, until=b"END"):
        """
        Sends a command to the telnet connection and reads until END
        is reached.

        :param command: command to send
        :type command: str

        :param until: byte delimiter string for reading command output
        :type until: byte str

        :return: response read
        :rtype: list
        """
        # leap_assert(self._tn, "We need a tn connection!")

        try:
            self._tn.write("%s\n" % (command,))
            buf = self._tn.read_until(until, 2)
            self._seek_to_eof()
            blist = buf.split('\r\n')
            if blist[-1].startswith(until):
                del blist[-1]
                return blist
            else:
                return []

        except socket.error, msg:
            # XXX should get a counter and repeat only
            # after mod X times.
            logger.warning('socket error %s (command was: "%s")' % (msg, command,))
            self._close_socket(announce=False)
            logger.debug('trying to reconnect to management')
            self.connect(self._socket_host, self._soccet_port)
            return []

        # XXX should move this to a errBack!
        except Exception as e:
            logger.warning("Error sending command %s: %r" %
                           (command, e))
        return []

    def _close_socket(self, announce=True):
        """
        Close connection to openvpn management interface.
        """
        logger.debug('closing socket')
        if announce:
            self._tn.write("quit\n")
            self._tn.read_all()
        self._tn.get_socket().close()
        self._tn = None

    def connect(self, socket_host, socket_port):
        """
        Connects to the management interface on the specified
        socket_host socket_port.

        :param socket_host: either socket path (unix) or socket IP
        :type socket_host: str

        :param socket_port: either string "unix" if it's a unix
                            socket, or port otherwise
        :type socket_port: str
        """
        # cache for reconnecting
        self._socket_host = socket_host
        self._socket_port = socket_port

        if self.is_connected:
            self._close_socket()

        try:
            self._tn = UDSTelnet(socket_host, socket_port)

            # XXX make password optional
            # specially for win. we should generate
            # the pass on the fly when invoking manager
            # from conductor

            # self.tn.read_until('ENTER PASSWORD:', 2)
            # self.tn.write(self.password + '\n')
            # self.tn.read_until('SUCCESS:', 2)
            if self._tn:
                self._tn.read_eager()

        # XXX move this to the Errback
        except Exception as e:
            logger.warning("Could not connect to OpenVPN yet: %r" % (e,))
            self._tn = None

    @property
    def is_connected(self):
        """
        Returns the status of the management interface.

        :returns: True if connected, False otherwise
        :rtype: bool
        """
        return True if self._tn else False

    def terminate(self):
        try:
            logger.debug("Sending SIGTERM")
            self._tn.write("signal SIGTERM\n")
        except socket.error, msg:
            logger.debug('SIGTERM caused %s' % (msg,))
            self._close_socket(announce=False)

    def disconnect(self):
        self._close_socket(announce=True)

    def get_state(self):
        state = self._send_command("state")
        logger.debug(state)
        return state

    def get_status(self):
        status = self._send_command("status")
        logger.debug(status)
        return status
