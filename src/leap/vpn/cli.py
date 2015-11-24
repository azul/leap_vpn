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
import time

from twisted.internet import reactor

from leap.vpn import VPNManager
from leap.vpn.firewall import FirewallManager
from leap.vpn.utils import get_path_prefix


def wait(secs):
    print("Waiting {} seconds...".format(secs))
    time.sleep(secs)


def test_firewall():
    remotes = (  # XXX HACK picked manually from eip-service.json
        ("198.252.153.84", "1194"),
        ("46.165.242.169", "1194"),
    )

    firewall = FirewallManager(remotes)

    print("Firewall: starting...")
    fw_ok = firewall.start()
    if fw_ok:
        print("Firewall: started")
        # vpn_ok = vpn.start()
        print ("Here we would start VPN")
    else:
        print ("Firewall: Error starting.")
        return

    wait(1)
    print "Firewall: is up? -> " + str(firewall.is_up())
    wait(3)
    print("Firewall: stopping...")
    fw_ok = firewall.stop()
    print("Firewall: stopped.")
    wait(1)
    print "Firewall: is up? -> " + str(firewall.is_up())


def test_vpn():
    remotes = (  # XXX HACK picked manually from eip-service.json
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

    vpn = VPNManager(remotes, cert_path, key_path, ca_path, extra_flags)

    print("VPN: starting...")
    vpn_ok = vpn.start()
    if vpn_ok:
        print("VPN: started")
    else:
        print ("VPN: Error starting.")
        return

    return
    wait(1)
    print "VPN: is up? -> " + str(vpn.is_up())
    wait(3)
    print("VPN: stopping...")
    vpn_ok = vpn.stop()
    print("VPN: stopped.")
    wait(1)
    print "VPN: is up? -> " + str(vpn.is_up())


def main():
    # test_firewall()
    test_vpn()


if __name__ == "__main__":
    # main()
    reactor.callWhenRunning(reactor.callLater, 0, main)
    reactor.run()
