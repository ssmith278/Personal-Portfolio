from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='projects'),
    path('sorter-chart/', views.sorter_chart, name='sorter-chart'),
]