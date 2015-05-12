# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import subprocess
from PIL import Image


class Camera:
    def __init__(self):
        pass

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
        pass


class LocalCamera(Camera):
    def __init__(self):
        super().__init__()

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
        pass


class RemoteCamera(Camera):
    pass