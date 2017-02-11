from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, Template
from webapp.models import District, School

# Create your views here.

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'christians_test.html', context=None)
        
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

def index(request):
    return render_to_response('christians_test.html')

