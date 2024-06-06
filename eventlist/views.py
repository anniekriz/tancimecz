from django.shortcuts import render
from django.http import HttpResponse
from .models import Event

# Create your views here.

def homepage(request):
    return render(request, 'homepage.html')

def event_list(request):
    events = Event.objects.all().order_by('date_time')
    return render(request, 'eventlist.html', {'events': events})