from django.conf.urls import patterns, url
from interface import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = patterns("",
    url(r'^$', views.index, name = "index"),
    url(r'^chart/(?P<chart_title>[\w\-"]+)/$', views.chart, name='chart'),
    url(r'^waiting/$', views.waiting, name = "waiting"), 
    #url(r'^login/$', auth_views.login, name = "login"),
    #url(r'^logout/$', auth_views.logout, name = "logout"),
    #url(r'^admin/$', admin.site.urls),


    )
