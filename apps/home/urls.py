# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from apps.home import views

urlpatterns = [

    # The home page
    # path('', views.index, name='home'),
    # search app
    path('',  include('apps.search.urls')),
    # upload app
    path('',  include('apps.upload.urls')),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
] 
