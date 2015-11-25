#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cli.py
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
Command line interface app to use EIP
"""
import os

from colorama import init as color_init
from colorama import Fore
from twisted.internet import reactor

from leap.vpn import VPNManager
from leap.vpn import FirewallManager
from leap.vpn.utils import get_path_prefix


class EIPManager(object):
    def __init__(self, remotes, cert, key, ca, flags):
        """
        """
        self._firewall = FirewallManager(remotes)
        self._vpn = VPNManager(remotes, cert, key, ca, flags)

    def start(self):
        """TODO: Docstring for start.
        :returns: TODO

        """
        print(Fore.BLUE + "Firewall: starting..." + Fore.RESET)
        fw_ok = self._firewall.start()
        if not fw_ok:
            return False

        print(Fore.GREEN + "Firewall: started" + Fore.RESET)

        vpn_ok = self._vpn.start()
        if not vpn_ok:
            print (Fore.RED + "VPN: Error starting." + Fore.RESET)
            self._firewall.stop()
            print(Fore.GREEN + "Firewall: stopped." + Fore.RESET)
            return False

        print(Fore.GREEN + "VPN: started" + Fore.RESET)

    def stop(self):
        """TODO: Docstring for stop.

        :returns: TODO
        """
        print(Fore.BLUE + "Firewall: stopping..." + Fore.RESET)
        fw_ok = self._firewall.stop()

        if not fw_ok:
            print (Fore.RED + "Firewall: Error stopping." + Fore.RESET)
            return False

        print(Fore.GREEN + "Firewall: stopped." + Fore.RESET)
        print(Fore.BLUE + "VPN: stopping..." + Fore.RESET)

        vpn_ok = self._vpn.stop()
        if not vpn_ok:
            print (Fore.RED + "VPN: Error stopping." + Fore.RESET)
            return False

        print(Fore.GREEN + "VPN: stopped." + Fore.RESET)
        return True


def main():
    # XXX HACK picked manually from eip-service.json
    remotes = (
        ("198.252.153.84", "1194"),
        ("46.165.242.169", "1194"),
    )

    prefix = os.path.join(get_path_prefix(),
                          "leap/providers/demo.bitmask.net/keys")
    cert_path = key_path = prefix + "/client/openvpn.pem"
    ca_path = prefix + "/ca/cacert.pem"

    extra_flags = {
        "auth": "SHA1",
        "cipher": "AES-128-CBC",
        "keepalive": "10 30",
        "tls-cipher": "DHE-RSA-AES128-SHA",
        "tun-ipv6": "true",
    }

    eip = EIPManager(remotes, cert_path, key_path, ca_path, extra_flags)
    reactor.addSystemEventTrigger('before', 'shutdown', eip.stop)
    eip.start()


if __name__ == "__main__":
    color_init()
    reactor.callWhenRunning(reactor.callLater, 0, main)
    reactor.run()
