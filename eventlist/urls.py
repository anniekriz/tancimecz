from django.urls import path
from . import views

app_name = 'eventlist'

urlpatterns = [
    path('events/', views.event_list, name="event_list"),
    path('', views.homepage)
]