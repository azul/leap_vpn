# -*- coding: utf-8 -*-
# manager.py
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
VPN Manager
"""
import subprocess

# XXX this doesn't exist yet
from leap.common.constants import IS_MAC


class _TempEIPConfig(object):
    """Current EIP code on bitmask depends on EIPConfig object, this temporary
    implementation helps on the transition."""

    def __init__(self, flags, path, ports):
        self._flags = flags
        self._path = path
        self._ports = ports

    def get_gateway_ports(self, idx):
        return self._ports

    def get_openvpn_configuration(self):
        return self._flags

    def get_client_cert_path(self, providerconfig):
        return self._path


class VPNManager(object):

    def set_openvpn_flags(self, flags):
        self._flags = flags

    def start(self):
        ports = []
        path = ""
        temp_eipconfig = _TempEIPConfig(self._flags, path, ports)
        pass

    # def bitmask_root_vpn_down(self):
    def stop(self):
        """
        Bring openvpn down using the privileged wrapper.

        :returns: True if succeeded, False otherwise.
        :rtype: bool
        """
        if IS_MAC:
            # We don't support Mac so far
            return True

        exitCode = subprocess.call(["pkexec", self.BITMASK_ROOT,
                                    "openvpn", "stop"])
        return True if exitCode is 0 else False

    def kill(self):
        """
        Sends a kill signal to the openvpn process.
        """
        pass

    def terminate(self):
        """
        Stop the openvpn subprocess.

        Attempts to send a SIGTERM first, and after a timeout it sends a
        SIGKILL.
        """
        pass
