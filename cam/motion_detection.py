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

__author__ = 'brainflakes'

"""
THIS CODE IS FROM https://www.raspberrypi.org/forums/viewtopic.php?t=45235

THX TO @brainflakes
"""

import subprocess
import os
import time
from datetime import datetime
from PIL import Image

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

# Motion detection settings:
# Threshold (how much a pixel has to change by to be marked as "changed")
# Sensitivity (how many changed pixels before capturing an image)
# ForceCapture (whether to force an image to be captured every forceCaptureTime seconds)
threshold = 10
sensitivity = 20
forceCapture = True
forceCaptureTime = 60 * 60  # Once an hour

# File settings
saveWidth = 1280
saveHeight = 960
diskSpaceToReserve = 40 * 1024 * 1024  # Keep 40 mb free on disk

# Capture a small test image (for motion detection)
def captureTestImage():
    command = "raspistill -w %s -h %s -t 0 -e bmp -o -" % (100, 75)
    imageData = StringIO()
    imageData.write(subprocess.check_output(command, shell=True))
    imageData.seek(0)
    im = Image.open(imageData)
    buffer = im.load()
    imageData.close()
    return im, buffer


# Save a full size image to disk
def saveImage(width, height, diskSpaceToReserve):
    keepDiskSpaceFree(diskSpaceToReserve)
    time = datetime.now()
    filename = "capture-%04d%02d%02d-%02d%02d%02d.jpg" % (
    time.year, time.month, time.day, time.hour, time.minute, time.second)
    subprocess.call("raspistill -w 1296 -h 972 -t 0 -e jpg -q 15 -o %s" % filename, shell=True)
    print("Captured %s" % filename)


# Keep free space above given level
def keepDiskSpaceFree(bytesToReserve):
    if (getFreeSpace() < bytesToReserve):
        for filename in sorted(os.listdir(".")):
            if filename.startswith("capture") and filename.endswith(".jpg"):
                os.remove(filename)
                print("Deleted %s to avoid filling disk" % filename)
                if (getFreeSpace() > bytesToReserve):
                    return


# Get available disk space
def getFreeSpace():
    st = os.statvfs(".")
    du = st.f_bavail * st.f_frsize
    return du

# Get first image
image1, buffer1 = captureTestImage()

# Reset last capture time
lastCapture = time.time()

while (True):

    # Get comparison image
    image2, buffer2 = captureTestImage()

    # Count changed pixels
    changedPixels = 0
    for x in range(0, 100):
        for y in range(0, 75):
            # Just check green channel as it's the highest quality channel
            pixdiff = abs(buffer1[x, y][1] - buffer2[x, y][1])
            if pixdiff > threshold:
                changedPixels += 1

    # Check force capture
    if forceCapture:
        if time.time() - lastCapture > forceCaptureTime:
            changedPixels = sensitivity + 1

    # Save an image if pixels changed
    if changedPixels > sensitivity:
        lastCapture = time.time()
        saveImage(saveWidth, saveHeight, diskSpaceToReserve)

    # Swap comparison buffers
    image1 = image2
    buffer1 = buffer2
