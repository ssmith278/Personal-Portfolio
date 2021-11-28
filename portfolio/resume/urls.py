from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('message-sent/', views.message_sent, name='message-sent'),
]