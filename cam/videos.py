# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import glob
import os
import re

from PySpyX import settings


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


class MotionVideo:
    VIDEO_PATTERN = r'(\d{,4})-(\d{,2})-(\d{,2})_(\d{,2})-(\d{,2})-(\d{,4})'

    def __init__(self, file):
        self.file = file

        dirname, self.filename = os.path.split(file)
        matches = re.match(self.VIDEO_PATTERN, self.filename)

        if matches:
            self.year = int(matches.group(1))
            self.month = int(matches.group(2))
            self.day = int(matches.group(3))
            self.hour = int(matches.group(4))
            self.minute = int(matches.group(5))
            self.second = int(matches.group(6))


    @staticmethod
    def getAll(directory):
        """

        :param directory: string
        :return: MotionVideo[]
        """
        video_files = glob.glob(directory + "/*.mp4")
        videos = []

        for video_file in video_files:
            videos.append(MotionVideo(video_file))

        return videos


    def getCaptureDate(self):
        """

        :return: datetime
        """
        return datetime.datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)

    def getFormattedDate(self):
        """

        :return: string
        """
        date = self.getCaptureDate()

        return date.__format__("%d.%m.%Y %H:%M")

    def getVideoUrl(self):
        """
        :return: string
        """
        print(settings.MOTION_VIDEO_URL, self.filename)
        return "/%s/%s" % (settings.MOTION_VIDEO_URL, self.filename)
