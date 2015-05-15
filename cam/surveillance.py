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
import time


""" http://www.maketecheasier.com/setup-motion-detection-webcam-ubuntu/ -> Motion """


class Surveillance:
    """
    @type motionDetectionThread: SurveillanceDetectionThread
    @type camera: cam.camera.Camera
    """

    def __init__(self, camera):
        """
        :param camera: cam.camera.Camera
        """
        self.camera = camera
        self.motionDetectionThread = ManualSurveillanceDetectionThread(self)

    def startMotionDetection(self):
        if not self.motionDetectionIsStarted():
            self.motionDetectionThread.start()

    def stopMotionDetection(self):
        if self.motionDetectionIsStarted():
            self.motionDetectionThread.exit()

    def motionDetectionIsStarted(self):
        """
        :return: boolean
        """
        return \
            self.motionDetectionThread is None and \
            self.motionDetectionThread.isAlive()

    def toggleMotionDetection(self):
        if self.motionDetectionIsStarted():
            self.stopMotionDetection()
        else:
            self.startMotionDetection()


class SurveillanceDetectionThread(threading.Thread):
    """
    @type surveillance: Surveillance
    @type threshold: int
    @type sensitivity: int
    @type forceCapture: boolean
    @type forceCaptureTime: int
    """

    def __init__(self, surveillance, threshold=10, sensitivity=20, forceCapture=False, forceCaptureTime=60 * 60):
        """
        :param surveillance: Surveillance
        :param threshold: int
        :param sensitivity: int
        :param forceCapture: boolean
        :param forceCaptureTime: int
        """
        super().__init__()

        self.surveillance = surveillance
        self.threshold = threshold
        self.sensitivity = sensitivity
        self.forceCapture = forceCapture
        self.forceCaptureTime = forceCaptureTime


class ManualSurveillanceDetectionThread(SurveillanceDetectionThread):
    """
    @type lastCapture: time
    @type image1: PIL.Image.Image
    @type image2: PIL.Image.Image
    """

    def __init__(self, surveillance, threshold=10, sensitivity=20, forceCapture=False, forceCaptureTime=60 * 60):
        """
        :param surveillance: Surveillance
        :param threshold: int
        :param sensitivity: int
        :param forceCapture: boolean
        :param forceCaptureTime: int
        """
        super().__init__(surveillance, threshold, sensitivity, forceCapture, forceCaptureTime)

        self.lastCapture = None
        self.image1 = None
        self.image2 = None


    def run(self):
        self.detectMotion(self.surveillance.camera)

    def detectMotion(self, camera):
        """
        :param camera: cam.camera.Camera
        """
        # Get first image
        self.image1 = camera.getThumbnailImage()
        buffer1 = self.image1.load()

        # Reset last capture time
        self.lastCapture = time.time()

        while (True):
            # Get comparison image
            self.image2 = camera.getThumbnailImage()
            buffer2 = self.image2.load()

            (width, height) = self.image2.size

            # Count changed pixels
            changedPixels = 0
            for x in range(0, width):
                for y in range(0, height):
                    # Just check green channel as it's the highest quality channel
                    pixdiff = abs(buffer1[x, y][1] - buffer2[x, y][1])
                    if pixdiff > self.threshold:
                        changedPixels += 1

            # Check force capture
            if self.forceCapture:
                if time.time() - self.lastCapture > self.forceCaptureTime:
                    changedPixels = self.sensitivity + 1

            # Trigger onMotion if motion detected
            if changedPixels > self.sensitivity:
                self.onMotion()

            # Swap comparison buffers
            self.image1 = self.image2

    def onMotion(self):
        self.lastCapture = time.time()
        # todo capture video