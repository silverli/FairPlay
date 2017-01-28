from __future__ import unicode_literals

from django.db import models

class District (models.Model):
    id = models.PositiveIntegerField(primary=True)
    name = models.CharField(max_length=100)

class School (models.Model):
    district = models.ForeignKey(District)
    composite_id = models.PositiveIntegerField(primary=True)
    name = models.CharField(max_length=200)
    school_id = models.CharField(max_length=20)
    county = models.CharField(max_length=100)
    
class GradeEnrollment (models.Model):
    school = models.ForeignKey(School)
    school_year = models.CharField(max_length=15)
    grade_level = models.CharField(max_length=25)
    boys = models.PositiveIntegerField()
    girls = models.PositiveIntegerField()
    
class SportsEnrollment (models.Model):
    school = models.ForeignKey(School)
    grade_level = models.CharField(max_length=25)
    school_year = models.CharField(max_length=15)
    sport = models.CharField(max_length=100)
    girls = models.PositiveIntegerField()
    boys = models.PositiveIntegerField()
    students = models.PositiveIntegerField()
    is_highschool = models.NullBooleanField()
    competetions_scheduled = models.PositiveIntegerField()
    competions_played = models.PositiveIntegerField()
    