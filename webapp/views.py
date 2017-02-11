from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, Template

from webapp.models import District, School, GradeEnrollment, SportsEnrollment


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
    school = School.objects.filter(composite_id = schoolid)
    schoolyear="2014-2015"
    data_ge = GradeEnrollment.objects.filter(school = school, school_year=schoolyear)
    data_se = SportsEnrollment.objects.filter(school = school, school_year=schoolyear)
 
    for result in data_ge:
        b = result.boys
        g = result.girls
    for result in data_se:
        b_ath = result.boys
        g_ath = result.girls
        t_ath = g_ath + b_ath
        t = b + g
        
    prop_g = g / t * 100
    prop_fsa = g_ath / t_ath * 100
    new_needed = g / t * t_ath - g_ath # number of opportunities needed to achieve equity
    multiplier = prop_g / 5 # i.e. your school is X times more than the legal gap
    
    return render_to_response('school_view.html',{
        "schools":school,
        "opportunities_needed":new_needed,
        "cheerleading_num1":5,
        "cheerleading_num2":7,
        "state_avg":15,
        "highsc_avg":19,
        "boys":b,
        "girls":g,
        "boy_ath":b_ath,
        "girl_ath":g_ath
    })