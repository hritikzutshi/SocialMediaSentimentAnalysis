from django.urls import path
from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.trending,name='trending'),
    path('history',views.history, name='history'),
    path('demo',views.demo, name='demo'),
    path('home',views.home, name='home'),
    path('aboutus',views.aboutus, name='aboutus'),
    path('map',views.map, name='map'),
    path('covid',views.covid, name='covid'),
    path('pb1',views.pb1, name='pb1'),
    path('covidstat',views.covidstat, name='covidstat'),
    path('piechart',views.piechart, name='piechart'),
    path('world',views.world, name='world'),
    path('states',views.states, name='states'),
    path('external', views.external,name="script"),
    path('algo', views.external,name="algo"),
    path('compn', views.compn,name="compn"),
    path('worldcomp', views.worldcomp,name='worldcomp')
]
