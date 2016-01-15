# coding: utf-8

import json
import subprocess
import time

from channels import Channel
from django.http import HttpResponse

from tasks.models import TaskRun
from tasks.utils import build_exception_response


def task_consumer(message):
    try:
  #    time.sleep(10)
      cmd = message.content['cmd_line'].split() 
      out = subprocess.check_output(cmd)
      taskrun = TaskRun.objects.get(pk=message.content['taskrun_pk'])
      taskrun.progress = 100
      taskrun.result = out
      taskrun.full_clean()
      taskrun.save()
      Channel('task_result-channel').send(json.loads(out))      
  #    print out
  #    cmd = "doit -f /Dati/dataflow/doit/topo.py --reporter json {}".format(message.content['task_name'])
  #    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1)
  #    for line in iter(proc.stdout.readline, b''):
  #        print line.strip()
    except Exception, exc:
      res = build_exception_response().data
      taskrun = TaskRun.objects.get(pk=message.content['taskrun_pk'])
      taskrun.progress = -100
      taskrun.result = res
      taskrun.full_clean()
      taskrun.save()
      Channel('task_result-channel').send(res)

def task_result_consumer(message):
    print message.content

def taskrun_consumer(message):
    print message.content
