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
from twisted.internet import reactor

from leap.vpn import EIPManager
from leap.vpn.utils import get_path_prefix


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
