# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 01:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='GradeEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_year', models.CharField(max_length=15)),
                ('grade_level', models.CharField(max_length=32)),
                ('boys', models.PositiveIntegerField()),
                ('girls', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('composite_id', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('school_id', models.CharField(max_length=20)),
                ('county', models.CharField(max_length=100)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.District')),
            ],
        ),
        migrations.CreateModel(
            name='SportsEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_level', models.CharField(max_length=32)),
                ('school_year', models.CharField(max_length=15)),
                ('sport', models.CharField(max_length=100)),
                ('girls', models.PositiveIntegerField()),
                ('boys', models.PositiveIntegerField()),
                ('students', models.PositiveIntegerField()),
                ('is_highschool', models.NullBooleanField()),
                ('gender', models.CharField(max_length=100)),
                ('competetions_scheduled', models.PositiveIntegerField()),
                ('competions_played', models.PositiveIntegerField()),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.School')),
            ],
        ),
        migrations.CreateModel(
            name='TitleNineGap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_year', models.CharField(max_length=15)),
                ('gap', models.FloatField(null=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.School')),
            ],
        ),
        migrations.AddField(
            model_name='gradeenrollment',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.School'),
        ),
    ]