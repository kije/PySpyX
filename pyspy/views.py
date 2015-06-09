# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import RequestContext, loader

from cam.camera import LocalCamera, RemoteCamera
from pyspy.models import Camera


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



def index(request):
    cameras = []
    cameras.append(LocalCamera())
    for camera in Camera.objects.all():
        cameras.append(RemoteCamera(camera))

    template = loader.get_template('pyspy/index.html')
    context = RequestContext(request, dict_={
        "cameras": cameras
    })
    return HttpResponse(template.render(context))


def control_local_cam(request):
    if request.method == 'POST':
        cam = LocalCamera()
        back_redirect_response = redirect('pyspy.views.index')

        print(request.POST)

        if "stop" in request.POST:
            cam.stopAll()
            return back_redirect_response
        elif "stream_start" in request.POST:
            cam.stopAll()
            cam.startStreaming()
            # todo message to user
            return back_redirect_response
        elif "surveillance_start" in request.POST:
            cam.stopAll()
            cam.startSurveillance()
            # todo message to user
            return back_redirect_response

    return HttpResponseBadRequest(content=b"Bad request!")


def cam_status(request):
    cam = LocalCamera()

    return JsonResponse({
        'is_streaming': cam.isStreamOn(),
        'is_stream_reachable': cam.isStreamReachable(),
        'is_surveillance_on': cam.isSurveillanceOn(),
        'ip': cam.getIp(),
        'stream_url': cam.getStreamUrl()
    })


def add_camera(request):
    if "ip" in request.POST:
        ip = request.POST["ip"]
        name = request.POST["name"] if "name" in request.POST else None

        try:
            validate_ipv46_address(ip)

            try:
                cam = Camera.objects.get(ip=ip)

                # todo message to user?
                if name is not None:
                    cam.name = name
                    cam.save()
            except Camera.DoesNotExist:
                cam = Camera(ip=ip, name=name)
                cam.save()

            if cam:
                return redirect('pyspy.views.index')
        except ValidationError:
            pass  # todo message to user

    return HttpResponseBadRequest(content=b"Bad request!")


def delete_cam(request):
    if "cam" in request.POST:
        id = request.POST["cam"]

        try:
            cam = Camera.objects.get(pk=id)

            cam.delete()

            return redirect('pyspy.views.index')

        except Camera.DoesNotExist:
            # todo message to user
            pass

    return HttpResponseBadRequest(content=b"Bad request!")
