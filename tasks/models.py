# -*- coding: utf-8 -*-

import subprocess

from channels.channel import Channel
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from pip.cmdoptions import editable
from twisted.conch.telnet import EDIT

from tasks.utils import build_exception_response


##########################################################
# SHOULD GO INTO OicomDjango!!!
class WithAuthor(models.Model):    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        abstract = True

#################################################
### Entità di base
#################################################
class Common(models.Model):
  ord = models.IntegerField(null=False, blank=True, default=0)
  name = models.CharField(max_length=80, null=False)
  descr = models.CharField(max_length=2000, null=True, blank=True)
 
  def __unicode__(self):
    return self.name
    
  class Meta:
    ordering = ['ord','name']
    abstract = True
    
##########################################################
class TaskRun(models.Model):    
  CHOICES_PROGRESS = (
    (-100, _(u'Fallita')),
    ( -50, _(u'In ritardo')),
    (   0, _(u'Creata')),
    (  50, _(u'Partita')),
    ( 100, _(u'Completa')),
  )
  
  task = models.ForeignKey('Task', null=False, blank=False, editable=False)
  user = models.ForeignKey(User, null=True, blank=True)
  started = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  progress = models.IntegerField(null=False, choices=CHOICES_PROGRESS, default=0)  
  result = models.TextField(null=True, blank=True)
          
  class Meta:
    ordering = ['task','started']
    verbose_name = "Esecuzione procedura"
    verbose_name_plural = "Esecuzioni procedura"
          
  def save(self, *args, **kwargs):
    super(TaskRun, self).save(*args, **kwargs)
    #should send progress (or all fields) to WebSocket!!!
    Channel('taskrun-channel').send({'taskrun_pk': self.pk,'progress': self.progress})
          
  def start(self):
    self.progress = 50
    self.full_clean()
    self.save()      
    
  def fail(self,result):
    self.progress = -100
    self.result = result
    self.full_clean()
    self.save()      
    
  def success(self,result):
    self.progress = 100
    self.result = result
    self.full_clean()
    self.save()      
    
#################################################
class Task(Common,WithAuthor):
  content_type = models.ForeignKey(ContentType, null=True, blank=True, editable=False)
  max_run = models.IntegerField(null=False, blank=True, default=0)

  class Meta:
    verbose_name = "Procedura"
    verbose_name_plural = "Procedure"

  def save(self, *args, **kwargs):
    if not self.content_type:
      self.content_type = ContentType.objects.get_for_model(self.__class__)
    super(Task, self).save(*args, **kwargs)

  def start(self):
    taskrun = TaskRun.objects.create(task=self)
    Channel('task-channel').send({'taskrun_pk': taskrun.pk})
    return taskrun

  def run(self):
    raise NotImplementedError()
  
def task_consumer(message):
  taskrun = TaskRun.objects.get(pk=message.content['taskrun_pk'])
  if taskrun.progress == 0:
    try:
      model = taskrun.task.content_type.model_class()
      task = model.objects.get(pk=taskrun.task.pk)
      taskrun.start()
      taskrun.success(task.run())      
    except Exception, exc:
      taskrun.fail(build_exception_response().data)
              
#################################################
class ShellTask(Task):
  cmd_line = models.CharField(max_length=2000, null=False, blank=False)

  class Meta:
    verbose_name = "Procedura shell"
    verbose_name_plural = "Procedure shell"

  def run(self):
#    time.sleep(10)
    cmd = self.cmd_line.split() 
    return subprocess.check_output(cmd)
#    print out
#    cmd = "doit -f /Dati/dataflow/doit/topo.py --reporter json {}".format(message.content['task_name'])
#    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1)
#    for line in iter(proc.stdout.readline, b''):
#        print line.strip()
