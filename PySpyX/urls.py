# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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

"""PySpyX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url

urlpatterns = [
    url(r'^(?:index)?/?$', 'pyspy.views.index', name='index'),
    url(r'^archive/?$', 'pyspy.views.archive', name='archive'),
    url(r'^cam/local/control/', 'pyspy.views.control_local_cam', name='cam_local_control'),
    url(r'^cam/status/', 'pyspy.views.cam_status', name='cam_status'),
    url(r'^cam/add/', 'pyspy.views.add_camera', name='add_camera'),
    url(r'^cam/delete/', 'pyspy.views.delete_cam', name='delete_camera'),
    url(r'^' + re.escape(settings.MOTION_VIDEO_URL) + r'/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MOTION_VIDEO_DIRECTORY,
    }),
]
