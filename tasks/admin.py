# coding: utf-8

from django import forms
from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.admin.widgets import ForeignKeyRawIdWidget, \
  ManyToManyRawIdWidget
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.utils.encoding import smart_unicode
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from tasks.models import Task, ShellTask, ChannelTask


#################################################
### See: http://djangosnippets.org/snippets/2217/
# SHOULD GO INTO OicomDjango!!!
class VerboseForeignKeyRawIdWidget(ForeignKeyRawIdWidget):
    def label_for_value(self, value):
        key = self.rel.get_related_field().name
        try:
            obj = self.rel.to._default_manager.using(self.db).get(**{key: value})
            change_url = reverse(
                "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.object_name.lower()),
                args=(obj.pk,)
            )
            return '&nbsp;<strong><a href="%s">%s</a></strong>' % (change_url, escape(obj))
        except (ValueError, self.rel.to.DoesNotExist):
            return '???'

class VerboseManyToManyRawIdWidget(ManyToManyRawIdWidget):
    def label_for_value(self, value):
        values = value.split(',')
        str_values = []
        key = self.rel.get_related_field().name
        for v in values:
            try:
                obj = self.rel.to._default_manager.using(self.db).get(**{key: v})
                x = smart_unicode(obj)
                change_url = reverse(
                    "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.object_name.lower()),
                    args=(obj.pk,)
                )
                str_values += ['<strong><a href="%s">%s</a></strong>' % (change_url, escape(x))]
            except self.rel.to.DoesNotExist:
                str_values += [u'???']
        return u', '.join(str_values)

#################################################
### Entità di base
#################################################
class CommonAdmin(admin.ModelAdmin):
  save_on_top = True
  list_display = ('__unicode__','ord',)
  search_fields = ('name',)
  fieldsets = (
    (None, {
        'fields': (('name','ord',),)
    }),
    ('Descrizione', {
        'fields': ('descr',),
    }),
  )

  def formfield_for_dbfield(self, db_field, **kwargs):
    u"""
    For "descr_XX" fields, use a suitably large textarea widget
    """
    formfield = super(CommonAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    if db_field.name.startswith('descr'):
      attrs = formfield.widget.attrs or {}
      attrs.update({'cols': '80', 'rows': '10', 'style': 'width: 80em;'})        
      formfield.widget = forms.Textarea(attrs=attrs)
      
    #see: http://djangosnippets.org/snippets/2217/
    if db_field.name in self.raw_id_fields:
      kwargs.pop("request", None)
      reltype = db_field.rel.__class__.__name__
      if reltype == "ManyToOneRel":
        formfield.widget = VerboseForeignKeyRawIdWidget(db_field.rel, self.admin_site)
      elif reltype == "ManyToManyRel":
        formfield.widget = VerboseManyToManyRawIdWidget(db_field.rel, self.admin_site)
    return formfield  

#################################################
class TaskAdmin(CommonAdmin):
  list_display = CommonAdmin.list_display + ('max_run','async',)
  fieldsets = CommonAdmin.fieldsets + (
    (None, {
        'fields': ('max_run','async',)
    }),
  )    
#NOOO!!! Non voglio che si possano gestire i Task non effettivamente eseguibili!!!  
# admin.site.register(Task,TaskAdmin)

#################################################
class ShellTaskAdmin(TaskAdmin):
  list_display = TaskAdmin.list_display
  fieldsets = TaskAdmin.fieldsets + (
    (None, {
        'fields': ('cmd_line',)
    }),
  )    
admin.site.register(ShellTask,ShellTaskAdmin)

#################################################
class ChannelTaskAdmin(TaskAdmin):
  list_display = TaskAdmin.list_display
  fieldsets = TaskAdmin.fieldsets + (
    (None, {
        'fields': ('channel','message')
    }),
  )    
admin.site.register(ChannelTask,ChannelTaskAdmin)
