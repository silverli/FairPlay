from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, Template
from webapp.models import District, School, GradeEnrollment, SportsEnrollment

# Create your views here.
def title_nine_calc(school, school_year = None):
    
    if(not school_year):
        school_year = GradeEnrollment.objects.order_by('school_year').last().school_year
    
    enrollment = GradeEnrollment.objects.filter(school=school, school_year=school_year)
    sports_enrollment = SportsEnrollment.objects.filter(school=school, school_year=school_year).exclude(girls=0, boys=0)
    
    if(not sports_enrollment):
        return False
    
    total, girls = 0, 0
    
    for grade_level in enrollment:
        total += grade_level.boys + grade_level.girls
        girls += grade_level.girls
        
    percent_girls_enrolled = (float(girls) / float(total))*100

    total_athletes, girl_athletes = 0, 0
    
    for sport in sports_enrollment:
        total_athletes += sport.girls + sport.boys
        girl_athletes += sport.girls

    girl_athlete_percentage = (float(girl_athletes) / float(total_athletes))*100
    
    return percent_girls_enrolled - girl_athlete_percentage
    

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'christians_test.html', context=None)
        
    def post(self, request, **kwargs):
        search, schools = None, None
        try:
            search = request.POST.get('search')
            schools = School.objects.filter(name__istartswith=search)
        except:
            pass
    
        return render(request, 'christians_test.html',{
            "schools":schools,
            "search":search
        })
    
def action(request):
    return render(request, 'action.html', context=None)
