from django.conf.urls import url
from webapp import views

urlpatterns = [
    url(r'^school_view/(?P<schoolid>([0-9]+))/?$', views.school_view, name='school_view'),
    url(r'^$', views.HomePageView.as_view()),
    url(r'^take_action/$', views.TakeActionPageView.as_view()),
    url(r'^donate/$', views.DonatePageView.as_view()),
    # url(r'^', views.index)
]