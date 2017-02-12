from __future__ import unicode_literals

from django.db import models


# Each model needs its own csv
# District needs to go in first, followed by School
# After that, it doesn't matter


class District (models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return '%s %s' % (self.id, self.name)

class School (models.Model):
    district = models.ForeignKey(District)
    composite_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    school_id = models.CharField(max_length=20)
    county = models.CharField(max_length=100)
    
    def __str__(self):
        return '%s - %s' % (self.district.name, self.name)
    
class GradeEnrollment (models.Model):
    school = models.ForeignKey(School)
    school_year = models.CharField(max_length=15)
    grade_level = models.CharField(max_length=32)
    boys = models.PositiveIntegerField()
    girls = models.PositiveIntegerField()
    
    def __str__(self):
        return '%s - %s - %s' % (self.school.name, self.grade_level, self.school_year)
    
class SportsEnrollment (models.Model):
    school = models.ForeignKey(School)
    grade_level = models.CharField(max_length=32)
    school_year = models.CharField(max_length=15)
    sport = models.CharField(max_length=100)
    girls = models.PositiveIntegerField()
    boys = models.PositiveIntegerField()
    students = models.PositiveIntegerField()
    is_highschool = models.NullBooleanField()
    gender = models.CharField(max_length=100) 
    competetions_scheduled = models.PositiveIntegerField()
    competions_played = models.PositiveIntegerField()
    
    def __str__(self):
        return '%s - %s - %s' % (self.school.name, self.grade_level, self.sport)

class TitleNineGap (models.Model):
    school = models.BigIntegerField()
    school_year = models.CharField(max_length=15)
    gap = models.FloatField(null=True)