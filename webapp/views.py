from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, Template
from webapp.models import District, School, GradeEnrollment, SportsEnrollment, TitleNineGap


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
        
    try:
        percent_girls_enrolled = (float(girls) / float(total))*100
    except:
        return False

    total_athletes, girl_athletes = 0, 0
    
    for sport in sports_enrollment:
        total_athletes += sport.girls + sport.boys
        girl_athletes += sport.girls

    try:
        girl_athlete_percentage = (float(girl_athletes) / float(total_athletes))*100
    except:
        return False
    
    return percent_girls_enrolled - girl_athlete_percentage

# Create your views here.

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)
        
    def post(self, request, **kwargs):
        search, schools = None, None
        try:
            search = request.POST.get('search')
            schools = School.objects.filter(name__istartswith=search)
        except:
            pass
    
        return render(request, 'index.html',{
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

def school_gaps():
    year_one = "2012-2013"
    year_two =  "2013-2014"
    year_three = "2014-2015"

    schools = School.objects.all()
    
    for school in schools:
        gap1 = title_nine_calc(school, year_one)
        gap2 = title_nine_calc(school, year_two)
        gap3 = title_nine_calc(school, year_three)
        
        print gap1, gap2, gap3
        
        TitleNineGap.objects.create(school=school.composite_id, school_year=year_one, gap=gap1)
        TitleNineGap.objects.create(school=school.composite_id, school_year=year_two, gap=gap2)
        TitleNineGap.objects.create(school=school.composite_id, school_year=year_three, gap=gap3)



def school_view(request,schoolid):
    school = School.objects.get(composite_id = schoolid)
    schoolyear="2014-2015"
    data_ge = GradeEnrollment.objects.filter(school = school, school_year=schoolyear)
    data_se = SportsEnrollment.objects.filter(school = school, school_year=schoolyear).exclude(girls=0,boys=0)

    gap_list = [round(TitleNineGap.objects.get(school_year='2012-2013', school = School.objects.get(composite_id = schoolid).composite_id).gap,2), round(TitleNineGap.objects.get(school_year='2013-2014', school = School.objects.get(composite_id = schoolid).composite_id).gap,2), round(TitleNineGap.objects.get(school_year='2014-2015', school = School.objects.get(composite_id = schoolid).composite_id).gap,2)]


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
    total_athletes = float(total_athletes)
    proportion_girls = float(proportion_girls)
    proportion_girls_athletes = float(proportion_girls_athletes)
    girls_athletes = float(girls_athletes)
    total_students = float(total_students)
    new_needed = float(new_needed)
    total_girls = float(total_girls)
    total_students = float(total_students)
    total_boys = float(total_boys)
    total_students = total_boys + total_girls
    proportion_girls = total_girls / total_students * 100
    proportion_girls_athletes= girls_athletes / total_athletes * 100
    new_needed = total_girls / total_students * total_athletes - girls_athletes # number of opportunities needed to achieve equity

    # calculate the statewide avg
    from django.db.models import Avg
    avg_gap_1213 = 0
    avg_gap_1314 = 0
    avg_gap_1415 = 0
    avg_gap_1213 = TitleNineGap.objects.filter(school_year='2012-2013').aggregate(Avg('gap'))
    avg_gap_1314 = TitleNineGap.objects.filter(school_year='2013-2014').aggregate(Avg('gap'))
    avg_gap_1415 = TitleNineGap.objects.filter(school_year='2014-2015').aggregate(Avg('gap'))
    state_avg_list = [avg_gap_1213, avg_gap_1314, avg_gap_1415]

    
    
    total_boys = int(total_boys)
    total_girls = int(total_girls)
    girls_athletes = int(girls_athletes)
    boys_athletes = int(boys_athletes)
    new_needed = int(new_needed)
    
    return render_to_response('school_view.html',{
        "school":school,
        "opportunities_needed":new_needed,
        "cheerleading_num1":5,
        "cheerleading_num2":7,
        "state_avg":state_avg_list[1],
        "highsc_avg":19,
        "boys":total_boys,
        "girls":total_girls,
        "boy_ath":boys_athletes,
        "girl_ath":girls_athletes,
        "title_nine_gap":gap_list
    })