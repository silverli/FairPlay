from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, Template
from webapp.models import District, NewSchool, GradeEnrollment, SportsEnrollment, TitleNineGap
from django.db.models import Avg

def title_nine_calc(school, school_year = None):
    
    if(not school_year):
        school_year = GradeEnrollment.objects.order_by('school_year').last().school_year
    
    enrollment = GradeEnrollment.objects.filter(real_school=school, school_year=school_year)
    sports_enrollment = SportsEnrollment.objects.filter(real_school=school, school_year=school_year).exclude(girls=0, boys=0)
    
    if(not sports_enrollment):
        return False
    
    total, girls = 0, 0
    
    for grade_level in enrollment:
        total += grade_level.boys + grade_level.girls
        girls += grade_level.girls
        print "girls ", grade_level.girls, "boys ", grade_level.boys
        
    print "total girls", girls, "total ", total
    try:
        percent_girls_enrolled = (float(girls) / float(total))*100
    except:
        return False

    total_athletes, girl_athletes = 0, 0
    
    print "########### athletes ################"
    for sport in sports_enrollment:
        total_athletes += sport.girls + sport.boys
        girl_athletes += sport.girls
        print "girls ", sport.girls, "boys ", sport.boys

    print "total girls", girl_athletes, "total athletes", total_athletes

    try:
        girl_athlete_percentage = (float(girl_athletes) / float(total_athletes))*100
    except:
        return False
    
    print "%enrolled", percent_girls_enrolled, "%athlete", girl_athlete_percentage
    
    return percent_girls_enrolled - girl_athlete_percentage

# Create your views here.

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)
        
    def post(self, request, **kwargs):
        search, schools = None, None
        try:
            search = request.POST.get('search')
            schools = NewSchool.objects.filter(name__istartswith=search)
        except:
            pass
    
        return render(request, 'index.html',{
            "schools":schools,
            "search":search
        })

    
class TakeActionPageView(TemplateView):
    template_name = "take_action.html"
    
        
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

    schools = NewSchool.objects.all()
    
    
    for school in schools:
        gap1 = title_nine_calc(school, year_one)
        gap2 = title_nine_calc(school, year_two)
        gap3 = title_nine_calc(school, year_three)
        
        print gap1, gap2, gap3
        
        TitleNineGap.objects.create(real_school=school, school_year=year_one, gap=gap1)
        TitleNineGap.objects.create(real_school=school, school_year=year_two, gap=gap2)
        TitleNineGap.objects.create(real_school=school, school_year=year_three, gap=gap3)



def school_view(request,schoolid):
    school = NewSchool.objects.get(composite_id = schoolid)
    schoolyear="2014-2015"
    data_ge = GradeEnrollment.objects.filter(real_school = school, school_year=schoolyear)
    data_se = SportsEnrollment.objects.filter(real_school = school, school_year=schoolyear).exclude(girls=0,boys=0)

    gap1 = round(TitleNineGap.objects.get(school_year='2012-2013', real_school=school).gap,2)
    gap2 = round(TitleNineGap.objects.get(school_year='2013-2014', real_school=school).gap,2)
    gap3 = round(TitleNineGap.objects.get(school_year='2014-2015', real_school=school).gap,2)
    gap_list = [gap1, gap2, gap3]


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
    # proportion_girls = total_girls / total_students * 100
#    proportion_girls_athletes= girls_athletes / total_athletes * 100
    # new_needed = total_girls / total_students * total_athletes - girls_athletes # number of opportunities needed to achieve equity

    # calculate the statewide avg
    
    avg_gap_1213 = 0
    avg_gap_1314 = 0
    avg_gap_1415 = 0
    avg_gap_1213 = TitleNineGap.objects.filter(school_year='2012-2013').aggregate(Avg('gap'))
    avg_gap_1314 = TitleNineGap.objects.filter(school_year='2013-2014').aggregate(Avg('gap'))
    avg_gap_1415 = TitleNineGap.objects.filter(school_year='2014-2015').aggregate(Avg('gap'))
    state_avg_list = [avg_gap_1213, avg_gap_1314, avg_gap_1415]

    avg_county_gap_1213 = 0
    avg_county_gap_1314 = 0
    avg_county_gap_1415 = 0
    avg_county_gap_1213 = TitleNineGap.objects.filter(school_year='2012-2013',real_school__county=school.county).aggregate(Avg('gap'))
    avg_county_gap_1314 = TitleNineGap.objects.filter(school_year='2013-2014',real_school__county=school.county).aggregate(Avg('gap'))
    avg_county_gap_1415 = TitleNineGap.objects.filter(school_year='2014-2015',real_school__county=school.county).aggregate(Avg('gap'))
    county_avg_list = [avg_county_gap_1213, avg_county_gap_1314, avg_county_gap_1415]
    
    total_boys = int(total_boys)
    total_girls = int(total_girls)
    girls_athletes = int(girls_athletes)
    boys_athletes = int(boys_athletes)
    new_needed = int(new_needed)

    print "TOTAL BOYS AND GIRLS", total_boys, total_girls
    return render_to_response('school_view.html',{
        "school":school,
        # "opportunities_needed":new_needed,
        # "cheerleading_num1":5,
        # "cheerleading_num2":7,
        "state_avg1":state_avg_list[0],
        "state_avg2":state_avg_list[1],
        "state_avg3":state_avg_list[2],
        "county_avg1":county_avg_list[0],
        "county_avg2":county_avg_list[1],
        "county_avg3":county_avg_list[2],
        # "highsc_avg":19,
        "boys":total_boys,
        "girls":total_girls,
        "boy_ath":boys_athletes,
        "girl_ath":girls_athletes,
        "title_nine_gap1":gap_list[0],
        "title_nine_gap2":gap_list[1],
        "title_nine_gap3":gap_list[2]
        
    })