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

import threading


""" http://www.maketecheasier.com/setup-motion-detection-webcam-ubuntu/ -> Motion """


class Motion:
    motionDetectionThread = None

    def __init__(self):
        motionDetectionThread = MotionDetectionThread(self)
        pass

    def startMotionDetection(self):
        if not self.motionDetectionIsStarted():
            self.motionDetectionThread.start()

    def stopMotionDetection(self):
        if self.motionDetectionIsStarted():
            self.motionDetectionThread.exit()

    def motionDetectionIsStarted(self):
        """
        :rtype boolean
        """
        return self.motionDetectionThread != None and \
               self.motionDetectionThread.isAlive()

    def toggleMotionDetection(self):
        if self.motionDetectionIsStarted():
            self.stopMotionDetection()
        else:
            self.startMotionDetection()


class MotionDetectionThread(threading.Thread):
    """
    @type motion: Motion
    """
    motion = None

    def __init__(self, motion):
        """
        :param motion: Motion
        """
        super().__init__()
        self.motion = motion

    def run(self):
        pass
