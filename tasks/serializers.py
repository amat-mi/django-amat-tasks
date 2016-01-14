# coding: utf-8

from rest_framework import serializers

from tasks.models import Task


#################################################
class TaskSerializer(serializers.ModelSerializer):
  pass

  class Meta:
    model = Task
