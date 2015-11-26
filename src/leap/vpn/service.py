#!/usr/bin/env python
# -*- coding: utf-8 -*-
# service.py
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
EIP service declaration.
"""
import os

from twisted.application import service
from twisted.python import log

from leap.vpn import EIPManager
from leap.vpn.utils import get_path_prefix


class HookableService(object):

    """
    This service allows for other services to be notified
    whenever a certain kind of hook is triggered.

    During the service composition, one is expected to register
    a kind of hook with the service that wants to react to the triggering of
    the hook. On that service, the method "notify_hook" will be called,
    which will be in turn dispatched to the method "hook_<name>".

    This is a simplistic implementation for a PoC, we probably will move
    this to another mechanism like leap.common.events, callbacks etc.
    """

    def register_hook(self, kind, trigger):
        if not hasattr(self, 'service_hooks'):
            self.service_hooks = {}
        log.msg("Registering hook %s->%s" % (kind, trigger))
        self.service_hooks[kind] = trigger

    def get_sibling_service(self, kind):
        return self.parent.getServiceNamed(kind)

    def get_hooked_service(self, kind):
        hooks = self.service_hooks
        if kind in hooks:
            return self.get_sibling_service(hooks[kind])

    def notify_hook(self, kind, **kw):
        if kind not in self.subscribed_to_hooks:
            raise RuntimeError(
                "Tried to notify a hook this class is not "
                "subscribed to" % self.__class__)
        getattr(self, 'hook_' + kind)(**kw)


class EIPService(service.Service, HookableService):

    def __init__(self):
        super(EIPService, self).__init__()

        # XXX picked manually from eip-service.json
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

        self._eip = EIPManager(remotes, cert_path, key_path, ca_path,
                               extra_flags)

    def startService(self):
        print "Starting EIP Service..."
        super(EIPService, self).startService()
        self._eip.start()

    def stopService(self):
        print "Stopping EIP Service..."
        super(EIPService, self).stopService()
        self._eip.stop()
