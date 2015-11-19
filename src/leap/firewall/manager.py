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
Firewall Manager
"""
import commands
import subprocess

# XXX this doesn't exist yet
from leap.common.constants import IS_MAC


class FirewallManager(object):

    BITMASK_ROOT = ""  # TODO add the bitmask-root path here

    # def _launch_firewall(self, gateways, restart=False):
    def start(self, gateways, restart=False):
        """
        Launch the firewall using the privileged wrapper.

        :param gateways: the gateway(s) that we will allow
        :type gateways: list

        :returns: True if the exitcode of calling the root helper in a
                  subprocess is 0.
        :rtype: bool
        """
        # XXX check for wrapper existence, check it's root owned etc.
        # XXX check that the iptables rules are in place.
        cmd = ["pkexec", self.BITMASK_ROOT, "firewall", "start"]
        if restart:
            cmd.append("restart")
        exitCode = subprocess.call(cmd + gateways)
        return True if exitCode is 0 else False

    # def tear_down_firewall(self):
    def stop(self):
        """
        Tear the firewall down using the privileged wrapper.
        """
        if IS_MAC:
            # We don't support Mac so far
            return True

        exitCode = subprocess.call(["pkexec", self.BITMASK_ROOT,
                                    "firewall", "stop"])
        return True if exitCode is 0 else False
        pass

    # def is_fw_down(self):
    def is_up(self):
        """
        Return whether the firewall is up or not.

        :rtype: bool
        """
        # TODO test this, refactored from is_fw_down

        cmd = "pkexec {0} firewall isup".format(self.BITMASK_ROOT)
        output = commands.getstatusoutput(cmd)[0]

        return output != 256
