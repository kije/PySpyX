# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from cam.surveillance import Surveillance

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import subprocess
from PIL import Image
import netifaces
import socket

"""
Camera Surveillance tool for Raspberry Pi with Camera module Project in ICT M152.
Copyright (C) 2015  Kim D. Jeker

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = 'kije'


def isReachable(ip, port, timeout=5):
    """
    :param ip: string
    :param port: int
    :param timeout: float
    :return:
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(timeout)
            s.connect((ip, port))
            return True
        except socket.error as e:
            # todo maybe log
            return False


class Camera:
    CAM_STREAMING_PORT = 8554

    def __init__(self):
        self.__is_reachable = {}

    def getImage(self):
        """
        :return: PIL.Image.Image
        """
        pass

    def getThumbnailImage(self):
        """
        :return: PIL.Image.Image
        """
        pass

    def getStreamUrl(self):
        """
        :return: string
        """
        return "rtsp://%s:%d" % (self.getIp(), self.CAM_STREAMING_PORT)

    def getIp(self):
        """
        :return: string
        """
        pass

    def isRemote(self):
        """
        :return: boolean
        """
        pass

    def isStreamReachable(self):
        """
        Check if the stream is reachable
        :return: boolean
        """
        return self.isReachable(self.CAM_STREAMING_PORT)

    def isReachable(self, port, timeout=2):
        """
        returns if a port is reachable. result will be cached
        :param port: int
        :param timeout: float
        :return: boolean
        """
        if port not in self.__is_reachable:
            self.__is_reachable.update({port: isReachable(self.getIp(), port, timeout)})

        return self.__is_reachable[port]


class LocalCamera(Camera):
    """
    @type surveillance: Surveillance
    """

    def __init__(self):
        super().__init__()
        self.__is_reachable = {}
        self.surveillance = Surveillance(self)

    def getImage(self):
        command = "raspistill -t 0 -e bmp -o -"
        imageData = StringIO()
        imageData.write(subprocess.check_output(command, shell=True))
        imageData.seek(0)
        im = Image.open(imageData)
        imageData.close()
        return im

    def getThumbnailImage(self):
        command = "raspistill -w %s -h %s -t 0 -e bmp -o -" % (200, 150)
        imageData = StringIO()
        imageData.write(subprocess.check_output(command, shell=True))
        imageData.seek(0)
        im = Image.open(imageData)
        imageData.close()
        return im

    def getIp(self):
        """
        :return: string
        """
        interfaces = netifaces.interfaces()
        for i in interfaces:
            if i.startswith('lo'):
                continue

            iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
            if iface != None:
                for j in iface:
                    return j['addr']

    def isRemote(self):
        """
        :return: boolean
        """
        return False

    def isReachable(self, port, timeout=2):
        """
        returns if a port is reachable. result will be cached
        :param port: int
        :param timeout: float
        :return: boolean
        """
        if port not in self.__is_reachable:
            self.__is_reachable.update({port: isReachable('127.0.0.1', port, timeout)})  # faster

        return self.__is_reachable[port]

    def startStreaming(self):
        """
        Starts the stream (if not already started)
        """
        if not self.isStreamOn():
            pass


    def stopStreaming(self):
        """
        Stops the stream (if started)
        """
        if self.isStreamOn():
            pass

    def startSurveillance(self):
        """
        Starts the surveillance mode (if not already started)
        """
        if not self.isSurveillanceOn():
            self.surveillance.startMotionDetection()

    def stopSurveillance(self):
        """
        Stops the surveillance mode (if started)
        """
        if self.isSurveillanceOn():
            self.surveillance.stopMotionDetection()

    def stopAll(self):
        """
        Stops every activity (streaming, surveillance). Turns the camera "off"
        """
        self.stopSurveillance()
        self.stopStreaming()

    def isSurveillanceOn(self):
        """
        Check if surveillance mode is on
        :return: boolean
        """
        return self.surveillance.motionDetectionIsStarted()

    def isStreamOn(self):
        """
        Check if stream is started
        :return: boolean
        """
        # todo maybe check here if script already running instead of if the stream is reachable
        return self.isStreamReachable()



class RemoteCamera(Camera):
    """
    @type camera: pyspy.models.Camera
    """

    def __init__(self, camera):
        """
        :param camera: pyspy.models.Camera
        """
        super().__init__()
        self.camera = camera


    def getIp(self):
        """
        :return: string
        """
        return self.camera.ip

    def isRemote(self):
        """
        :return: boolean
        """
        return True

    def getImage(self):
        """
        :return: PIL.Image.Image
        """
        pass

    def getThumbnailImage(self):
        """
        :return: PIL.Image.Image
        """
        pass
