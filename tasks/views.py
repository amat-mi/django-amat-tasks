# coding: utf-8

from channels.channel import Channel
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.generic.base import View
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Task
from tasks.serializers import TaskSerializer
from tasks.utils import build_message_response, build_exception_response


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

#################################################
class TaskViewSet(viewsets.ReadOnlyModelViewSet):
  serializer_class = TaskSerializer
  queryset = Task.objects.all()
  paginate_by = None

  @detail_route(methods=['POST'])
  def run(self, request, pk=None):
    try:
      task = Task.objects.get(pk=pk)
      Task.run_this(task)
      return build_message_response('OK')
    except Exception, exc:
      return build_exception_response()
