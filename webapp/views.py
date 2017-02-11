from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, Template

from webapp.models import District, School, GradeEnrollment, SportsEnrollment

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

# Create your views here.

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
    
    
    
        
# def test_view(request):
#     query, schools = None, None
#     print request.GET.get('query')
#     try:
#         query = request.GET.get('query')
#         schools = School.objects.filter(name__istartswith=query)
#     except:
#         pass

#     return render_to_response('test_view_1.html',{
#         "schools":schools,
#         "query":query
#     })
    
# def second_view(request):
#     district = request.GET['query']

# def index(request):
#     return render_to_response('christians_test.html')

def school_view(request,schoolid):
    school = School.objects.get(composite_id = schoolid)
    schoolyear="2014-2015"
    data_ge = GradeEnrollment.objects.filter(school = school, school_year=schoolyear)
    data_se = SportsEnrollment.objects.filter(school = school, school_year=schoolyear).exclude(girls=0,boys=0)


    title_nine_gap = title_nine_calc(school)

    if title_nine_gap:
        title_nine_gap = round(title_nine_gap, 2)

    total_athletes=0
    boys_athletes=0
    girls_athletes=0
    total_students=0
    total_boys=0
    total_girls=0
    
    for result in data_ge:
        total_boys +=  result.boys
        total_girls += result.girls

    for result in data_se:
        boys_athletes += result.boys
        girls_athletes += result.girls
        total_athletes += result.students
    
   
    proportion_girls = 0
    proportion_girls_athletes = 0
    new_needed = 0
    multiplier = 0
    total_athletes = float(total_athletes)
    proportion_girls = float(proportion_girls)
    proportion_girls_athletes = float(proportion_girls_athletes)
    girls_athletes = float(girls_athletes)
    total_students = float(total_students)
    new_needed = float(new_needed)
    total_girls = float(total_girls)
    multiplier = float(multiplier)
    total_students = float(total_students)
    total_boys = float(total_boys)
    total_students = total_boys + total_girls
    proportion_girls = total_girls / total_students * 100
    proportion_girls_athletes= girls_athletes / total_athletes * 100
    new_needed = total_girls / total_students * total_athletes - girls_athletes # number of opportunities needed to achieve equity
    multiplier = title_nine_gap / 5 # i.e. your school is X times more than the legal gap
    
    total_boys = int(total_boys)
    total_girls = int(total_girls)
    girls_athletes = int(girls_athletes)
    boys_athletes = int(boys_athletes)
    new_needed = int(new_needed)
    multiplier = round(multiplier, 1)
    
    return render_to_response('school_view.html',{
        "school":school,
        "opportunities_needed":new_needed,
        "cheerleading_num1":5,
        "cheerleading_num2":7,
        "state_avg":15,
        "highsc_avg":19,
        "boys":total_boys,
        "girls":total_girls,
        "boy_ath":boys_athletes,
        "girl_ath":girls_athletes,
        "multiplier":multiplier,
        "title_nine_gap":title_nine_gap
    })