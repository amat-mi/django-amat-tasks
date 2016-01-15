# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-15 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20160114_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskrun',
            name='ended',
        ),
        migrations.AddField(
            model_name='taskrun',
            name='status',
            field=models.IntegerField(choices=[(-100, 'Fallito'), (-50, 'In ritardo'), (0, 'Partito'), (100, 'Completo')], default=0),
        ),
    ]