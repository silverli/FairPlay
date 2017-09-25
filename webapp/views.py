from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, Template
from webapp.models import District, NewSchool, GradeEnrollment, SportsEnrollment, TitleNineGap
from django.db.models import Avg

def titleix_zero_remover():
    reporters = SportsEnrollment.objects.all().exclude(girls=0,boys=0).distinct('real_school_id').values_list('real_school_id',flat=True)
    nonreporters = NewSchool.objects.all().exclude(id__in=reporters)
    TitleNineGap.objects.filter(real_school_id__in=nonreporters).update(gap=None)

    reporters = SportsEnrollment.objects.filter(school_year='2012-2013').exclude(girls=0,boys=0).distinct('real_school_id').values_list('real_school_id',flat=True)
    nonreporters = NewSchool.objects.all().exclude(id__in=reporters)
    TitleNineGap.objects.filter(real_school_id__in=nonreporters,school_year='2012-2013').update(gap=None)

    reporters = SportsEnrollment.objects.filter(school_year='2013-2014').exclude(girls=0,boys=0).distinct('real_school_id').values_list('real_school_id',flat=True)
    nonreporters = NewSchool.objects.all().exclude(id__in=reporters)
    TitleNineGap.objects.filter(real_school_id__in=nonreporters,school_year='2013-2014').update(gap=None)
    
    reporters = SportsEnrollment.objects.filter(school_year='2014-2015').exclude(girls=0,boys=0).distinct('real_school_id').values_list('real_school_id',flat=True)
    nonreporters = NewSchool.objects.all().exclude(id__in=reporters)
    TitleNineGap.objects.filter(real_school_id__in=nonreporters,school_year='2014-2015').update(gap=None)

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
        
    print "total girls", girls, "total ", total
    try:
        percent_girls_enrolled = (float(girls) / float(total))*100
    except:
        return False

    total_athletes, girl_athletes = 0, 0
    
    for sport in sports_enrollment:
        total_athletes += sport.girls + sport.boys
        girl_athletes += sport.girls
        print "girls ", sport.girls, "boys ", sport.boys


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
            schools = NewSchool.objects.filter(name__istartswith=search)
        except:
            pass
    
        return render(request, 'index.html',{
            "schools":schools,
            "search":search
        })

    
class TakeActionPageView(TemplateView):
    template_name = "take_action.html"

class DonatePageView(TemplateView):
    template_name = "donate.html"
    
        
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
        
        
    year_one = "2012-2013"
    year_two =  "2013-2014"
    year_three = "2014-2015"
    
    for school in schools:
        gap1 = title_nine_calc(school, year_one)
        gap2 = title_nine_calc(school, year_two)
        gap3 = title_nine_calc(school, year_three)
        
        
        TitleNineGap.objects.create(real_school=school, school_year=year_one, gap=gap1)
        TitleNineGap.objects.create(real_school=school, school_year=year_two, gap=gap2)
        TitleNineGap.objects.create(real_school=school, school_year=year_three, gap=gap3)



def school_view(request,schoolid):
    school = NewSchool.objects.get(composite_id = schoolid)
    schoolyear1="2012-2013"
    schoolyear2="2013-2014"
    schoolyear3="2014-2015"
    data_ge1 = GradeEnrollment.objects.filter(real_school = school, school_year=schoolyear1)
    data_se1 = SportsEnrollment.objects.filter(real_school = school, school_year=schoolyear1).exclude(girls=0,boys=0)
    
    data_ge2 = GradeEnrollment.objects.filter(real_school = school, school_year=schoolyear2)
    data_se2 = SportsEnrollment.objects.filter(real_school = school, school_year=schoolyear2).exclude(girls=0,boys=0)
    
    data_ge3 = GradeEnrollment.objects.filter(real_school = school, school_year=schoolyear3)
    data_se3 = SportsEnrollment.objects.filter(real_school = school, school_year=schoolyear3).exclude(girls=0,boys=0)

    
    gap1 = TitleNineGap.objects.get(school_year='2012-2013', real_school=school).gap
    gap2 = TitleNineGap.objects.get(school_year='2013-2014', real_school=school).gap
    gap3 = TitleNineGap.objects.get(school_year='2014-2015', real_school=school).gap
    
    
    if gap1 is not None:
        gap1 = round(gap1, 2)
    if gap2 is not None:
        gap2 = round(gap2, 2)
    if gap3 is not None:
        gap3 = round(gap3, 2)
    
    gap_list = [gap1, gap2, gap3]
    
    #2012-2013 data
    total_athletes1=0
    boys_athletes1=0
    girls_athletes1=0
    total_students1=0
    total_boys1=0
    total_girls1=0
    
    for result in data_ge1:
        total_boys1 +=  result.boys
        total_girls1 += result.girls

    for result in data_se1:
        boys_athletes1 += result.boys
        girls_athletes1 += result.girls
        total_athletes1 += result.students
    
    total_athletes1 = float(total_athletes1)
    girls_athletes1 = float(girls_athletes1)
    total_students1 = float(total_students1)
    total_girls1 = float(total_girls1)
    total_boys1 = float(total_boys1)
    total_students1 = total_boys1 + total_girls1
    
    #2013-2014 data
    total_athletes2=0
    boys_athletes2=0
    girls_athletes2=0
    total_students2=0
    total_boys2=0
    total_girls2=0
    
    for result in data_ge2:
        total_boys2 +=  result.boys
        total_girls2 += result.girls

    for result in data_se2:
        boys_athletes2 += result.boys
        girls_athletes2 += result.girls
        total_athletes2 += result.students
    
    total_athletes2 = float(total_athletes2)
    girls_athletes2 = float(girls_athletes2)
    total_students2 = float(total_students2)
    total_girls2 = float(total_girls2)
    total_boys2 = float(total_boys2)
    total_students2 = total_boys2 + total_girls2

    # 2014-2015 data
    total_athletes3=0
    boys_athletes3=0
    girls_athletes3=0
    total_students3=0
    total_boys3=0
    total_girls3=0
    
    for result in data_ge3:
        total_boys3 +=  result.boys
        total_girls3 += result.girls

    for result in data_se3:
        boys_athletes3 += result.boys
        girls_athletes3 += result.girls
        total_athletes3 += result.students
    
   
    proportion_girls3 = 0
    proportion_girls_athletes3 = 0
    new_needed3 = 0
    total_athletes3 = float(total_athletes3)
    proportion_girls3 = float(proportion_girls3)
    proportion_girls_athletes3 = float(proportion_girls_athletes3)
    girls_athletes3 = float(girls_athletes3)
    total_students3 = float(total_students3)
    new_needed3 = float(new_needed3)
    total_girls3 = float(total_girls3)
    total_boys3 = float(total_boys3)
    total_students3 = total_boys3 + total_girls3
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
    
    total_boys1 = int(total_boys1)
    total_girls1 = int(total_girls1)
    girls_athletes1 = int(girls_athletes1)
    boys_athletes1 = int(boys_athletes1)
    
    total_boys2 = int(total_boys2)
    total_girls2 = int(total_girls2)
    girls_athletes2 = int(girls_athletes2)
    boys_athletes2 = int(boys_athletes2)
    
    total_boys3 = int(total_boys3)
    total_girls3 = int(total_girls3)
    girls_athletes3 = int(girls_athletes3)
    boys_athletes3 = int(boys_athletes3)
    new_needed3 = int(new_needed3)

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
        "boys1":total_boys1,
        "girls1":total_girls1,
        "boy_ath1":boys_athletes1,
        "girl_ath1":girls_athletes1,
        "boys2":total_boys2,
        "girls2":total_girls2,
        "boy_ath2":boys_athletes2,
        "girl_ath2":girls_athletes2,
        "boys3":total_boys3,
        "girls3":total_girls3,
        "boy_ath3":boys_athletes3,
        "girl_ath3":girls_athletes3,
        "title_nine_gap1":gap_list[0],
        "title_nine_gap2":gap_list[1],
        "title_nine_gap3":gap_list[2]
        
    })