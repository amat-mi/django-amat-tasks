# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from channels.channel import Channel
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from twisted.conch.telnet import EDIT
from pip.cmdoptions import editable


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
    (   0, _(u'Partita')),
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
    Channel('taskrun-channel').send({'taskrun_pk': self.pk,'progress': self.progress})
          
def taskrun_consumer(message):
  print message.content         #should send to WebSocket!!!
  
  instance = TaskRun.objects.get(pk=message.content['taskrun_pk'])
  if instance.progress == 0:
    instance.task.run()
          
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

  def run(self):
    raise NotImplementedError()

  @classmethod
  def run_this(cls,instance):
    taskrun = TaskRun.objects.create(task=instance)
    Channel('task-channel').send({'taskrun_pk': taskrun.pk})
    return taskrun

  @classmethod
  def pippo(cls,instance):
    model = instance.content_type.model_class()
    task = model.objects.get(pk=instance.pk)
    taskrun = TaskRun.objects.create(task=task)
    return task.run(taskrun)
    
#################################################
class ShellTask(Task):
  cmd_line = models.CharField(max_length=2000, null=False, blank=False)

  class Meta:
    verbose_name = "Procedura shell"
    verbose_name_plural = "Procedure shell"

  def run(self,taskrun):
    Channel('task-channel').send({'taskrun_pk': taskrun.pk,'cmd_line': self.cmd_line})
    return taskrun
