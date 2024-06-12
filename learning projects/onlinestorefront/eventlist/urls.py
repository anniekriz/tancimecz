from django.urls import path
from . import views

app_name = 'eventlist'

urlpatterns = [
    path('events/', views.event_list, name="list"),
    path('search/', views.search_result, name="search"),
]