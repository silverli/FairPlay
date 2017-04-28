from django.contrib import admin
from webapp.models import District, School, GradeEnrollment, SportsEnrollment, TitleNineGap


# Register your models here.

admin.site.register(District)
admin.site.register(School)
admin.site.register(GradeEnrollment)
admin.site.register(SportsEnrollment)
admin.site.register(TitleNineGap)