# coding: utf-8

from channels.channel import Channel
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.generic.base import View
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response


#################################################
class DoitView(View):
  def get(self,request):
    Channel('slow-channel').send({'task_name': request.path[1:]})
    return HttpResponse("Hello world! You asked for {} with {}".format(request.path,request.method))

#################################################
class TaskView(APIView):
#     serializer_class = None
#     queryset = None
#     paginate_by = None

  def post(self, request, format=None):
    return Response("OK:{}".format(request.data))
