# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-11 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20170211_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titleninegap',
            name='school',
            field=models.BigIntegerField(),
        ),
    ]
