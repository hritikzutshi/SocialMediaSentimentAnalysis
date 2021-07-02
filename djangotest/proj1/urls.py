from django.urls import path
from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.trending,name='trending'),
    path('history',views.history, name='history'),
    path('home',views.home, name='home'),
    path('aboutus',views.aboutus, name='aboutus'),
    path('map',views.map, name='map'),
    path('covid',views.covid, name='covid'),
    path('pb1',views.pb1, name='pb1'),
    path('covidstat',views.covidstat, name='covidstat'),
    
    
]