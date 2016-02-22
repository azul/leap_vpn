#!/usr/bin/env python
# -*- coding: utf-8 -*-
# zmq_pub.py
# Copyright (C) 2016 LEAP
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
ZMQ Publisher for state changes on VPN FSM
"""
import Queue
import threading
import time

import zmq


class ZMQPublisher(object):
    def __init__(self, queue):
        self._worker_thread = threading.Thread(target=self._run)
        self._do_work = threading.Event()
        self._queue = queue

    def start(self):
        """
        Start the worker thread for the signaler server.
        """
        self._do_work.set()
        self._worker_thread.start()

    def _run(self):
        """
        Start a loop to process the ZMQ requests from the signaler client.
        """
        print "ZMQPublisher: loop started"

        port = "5556"
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://*:%s" % port)

        while self._do_work.is_set():
            try:
                data = self._queue.get()
                # print "Got data from queue: ", data
                socket.send_string("status: %s - data: %s".format(
                    data['status'], data['data']))
            except Queue.Empty:
                time.sleep(1)

        print "ZMQPublisher: loop stopped"

    def stop(self):
        """
        Stop the SignalerQt blocking loop.
        """
        self._do_work.clear()
