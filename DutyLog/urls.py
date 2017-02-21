#coding=utf-8
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^$', views.myadmin, name='index'),
    url(r'index', views.index, name="index2"),
    url(r'log_handler$', views.log_handler, name="log_handler"),
    url(r'myadmin$', views.myadmin, name="myadmin"),
    url(r'adduser$', views.adduser, name="adduser"),
    url(r'myadmin_login$', views.myadmin_login, name="myadmin_login"),
    url(r'archive$', views.archive, name="archive"),
    url(r'sign_in$', views.sign_in, name="sign_in"),
    url(r'get_sign_in_flag$', views.get_sign_in_flag, name="sign_in_flag"),
    url(r'search$', views.search, name="search"),
    url(r'get_dutyinfo_by_page_no$', views.get_dutyinfo_by_page_no, name="get_dutyinfo_by_page_no"),

]