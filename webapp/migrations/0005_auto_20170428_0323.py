# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-28 03:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20170428_0316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='titleninegap',
            name='real_school',
        ),
        migrations.RemoveField(
            model_name='titleninegap',
            name='school',
        ),
        migrations.DeleteModel(
            name='TitleNineGap',
        ),
    ]
