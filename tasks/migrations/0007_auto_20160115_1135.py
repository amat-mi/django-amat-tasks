# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-15 10:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20160115_1129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskrun',
            old_name='status',
            new_name='progress',
        ),
    ]
