# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 22:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectsApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='project',
            name='updated_at',
            field=models.DateTimeField(verbose_name='date updated'),
        ),
    ]
