from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^quotes$', views.quotes),
    url(r'^create$', views.create),
    url(r'^show/(?P<id>\d+)$', views.show),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^add/(?P<id>\d+)$', views.add),
    url(r'^logout$', views.logout),
]