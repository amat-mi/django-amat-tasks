# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-14 17:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('tasks', '0002_shelltask'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
