# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


##########################################################
# SHOULD GO INTO OicomDjango!!!
class WithAuthor(models.Model):    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        abstract = True

##########################################################
# SHOULD GO INTO OicomDjango!!!
class Downcasting(models.Model):    
    content_type = models.ForeignKey(ContentType, null=True, blank=True, editable=False)
  
    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(Downcasting, self).save(*args, **kwargs)
  
    class Meta:
        abstract = True

    _downcast = None
    @property
    def downcast(self):
        if not self._downcast: 
            self._downcast = self.content_type.model_class().objects.get(pk=self.pk)
        return self._downcast
    
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
    
#################################################
class DataContainer(Common,WithAuthor,Downcasting):
  url = models.CharField(max_length=500, null=False)

  class Meta:
    verbose_name = _("Contenitore dati")
    verbose_name_plural = _("Contenitori Dati")

#################################################
class Data(Common,WithAuthor,Downcasting):
  container = models.ForeignKey('DataContainer', related_name='data', null=False, blank=False)
  dependencies = models.ManyToManyField('self',through="DataTask",null=True, blank=True,
                                    symmetrical=False)

  class Meta:
    verbose_name = _("Dati")
    verbose_name_plural = _("Dati")

#################################################
class DataTask(models.Model):
  task = models.ForeignKey('tasks.Task',related_name='data',null=True, blank=True)
  data = models.ForeignKey('Data')
  dep = models.ForeignKey('Data',related_name='dependents')
  ord = models.IntegerField(null=True, blank=True, default=0)

  def __unicode__(self):
    return u'{} dipende da {} tramite {}'.format(self.data,self.dep,self.task)
  
  class Meta:
    verbose_name = _("Dipendenza")
    verbose_name_plural = _("Dipendenze")
    ordering = ['task','ord']
    