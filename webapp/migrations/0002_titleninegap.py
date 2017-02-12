# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-11 21:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TitleNineGap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_year', models.CharField(max_length=15)),
                ('gap', models.FloatField(null=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.School')),
            ],
        ),
    ]
