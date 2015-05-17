# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import os
import subprocess
import time

import picamera
import picamera.array
import numpy


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

""" http://bits.citrusbyte.com/motion-detection-with-raspberry-pi/ -> Motion detection """


class PiMotion:
    def __init__(self, verbose=False, post_capture_callback=None):
        self.verbose = verbose
        self.post_capture_callback = post_capture_callback

    def start(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (1280, 960)
            camera.framerate = 10

            handler = CaptureHandler(camera, self.post_capture_callback)

            print('Waiting 2 seconds for the camera to warm up')
            time.sleep(2)

            try:
                print('Started recording')
                # We can dump the actual video data since we don't use it
                camera.start_recording(
                    '/dev/null', format='h264',
                    motion_output=MyMotionDetector(camera, handler)
                )

                while True:
                    handler.tick()
                    time.sleep(1)
            finally:
                camera.stop_recording()
                print('Stopped recording')


class MyMotionDetector(picamera.array.PiMotionAnalysis):
    def __init__(self, camera, handler):
        super(MyMotionDetector, self).__init__(camera)
        self.handler = handler
        self.first = True

    # This method is called after each frame is ready for processing.
    def analyse(self, a):
        a = numpy.sqrt(
            numpy.square(a['x'].astype(numpy.float)) +
            numpy.square(a['y'].astype(numpy.float))
        ).clip(0, 255).astype(numpy.uint8)

        # If there are 50 vectors detected with a magnitude of 60.
        # We consider movement to be detected.
        if (a > 60).sum() > 50:
            # Ignore the first detection, the camera sometimes
            # triggers a false positive due to camera warmup.
            if self.first:
                self.first = False
                return

            # The handler is explained later in this article
            self.handler.motion_detected()


class CaptureHandler:
    def __init__(self, camera, post_capture_callback=None):
        self.camera = camera
        self.callback = post_capture_callback
        self.detected = False
        self.working = False
        self.i = 0

    def motion_detected(self):
        if not self.working:
            self.detected = True

    def tick(self):
        if self.detected:
            print("Started working on capturing")
            self.working = True
            self.detected = False
            self.i += 1

            path = "captures/%s/" % datetime.datetime.now().isoformat()

            os.mkdir(path)

            # Show the preview window on a connected display device
            self.camera.start_preview()

            # Take 16 photos to capture the movement
            for x in range(1, 16):
                filename = "detected-%02d.jpg" % x
                # Because we are continuously capturing video data
                # we have to use the video port to capture our photos
                self.camera.capture(path + filename, use_video_port=True)
                print("Captured " + filename)

            self.camera.stop_preview()

            print("Generating the montage")
            montage_file = path + 'montage.jpg'
            # We use imagemagick's montage to create a montage of the 16 photos
            # todo remove imagemagick dependency
            subprocess.call("montage -border 0 -background none -geometry 240x180 " + path + "* " + montage_file,
                            shell=True)

            print("Finished capturing")

            if self.callback:
                self.callback(montage_file)
                self.working = False
