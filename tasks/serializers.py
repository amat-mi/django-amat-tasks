# coding: utf-8

from rest_framework import serializers

from tasks.models import Task, TaskRun


#################################################
class TaskSerializer(serializers.ModelSerializer):
  pass

  class Meta:
    model = Task

#################################################
class TaskRunSerializer(serializers.ModelSerializer):
  pass

  class Meta:
    model = TaskRun
