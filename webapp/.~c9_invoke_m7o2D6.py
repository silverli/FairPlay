from django.shortcuts import render_to_response
from django.http import HttpResponse

from django.template import Context, Template

from webapp.models import District, School

# Create your views here.

def test_view(request):
    query, schools = None, None
    print request.GET.get('query')
    try:
        query = request.GET.get('query')
        schools = School.objects.filter(name__istartswith=query)
    except:
        pass

    return render_to_response('test_view_1.html',{
        "schools":schools,
        "query":query
    })
    
def second_view(request):
    district = request.GET['query']
    
    def second_view(request):
    district = request.GET['query']