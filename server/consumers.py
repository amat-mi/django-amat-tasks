# coding: utf-8

import json
import subprocess
import time

from channels import Channel
from django.http import HttpResponse


def http_consumer(message):
    Channel('slow-channel').send({'task_name': message.content['path'][1:]})
    response = HttpResponse("Hello world! You asked for {} with {}".format(message.content['path'],message.content['method']))
    message.reply_channel.send(response.channel_encode())

def slow_consumer(message):
#    time.sleep(10)
    out = subprocess.check_output(["doit", "-f" , "/Dati/dataflow/doit/topo.py", "--report", "json", message.content['task_name']])
    Channel('task_result-channel').send(json.loads(out))
#    print out
#    cmd = "doit -f /Dati/dataflow/doit/topo.py --reporter json {}".format(message.content['task_name'])
#    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1)
#    for line in iter(proc.stdout.readline, b''):
#        print line.strip()

def task_result_consumer(message):
    print message.content

def as_view_consumer(message):
    print message.content
