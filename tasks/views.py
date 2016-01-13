# coding: utf-8

from channels.channel import Channel
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.generic.base import View


#################################################
class DoitView(View):
  def get(self,request):
    Channel('slow-channel').send({'task_name': request.path[1:]})
    return HttpResponse("Hello world! You asked for {} with {}".format(request.path,request.method))
