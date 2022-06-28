from django.urls import path
from . import views


urlpatterns = [
    path('', views.search_gene, name="search"),
    path('api', views.postdata_api, name="api"),
]
