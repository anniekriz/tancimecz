from django.shortcuts import render
from danceapp.models import Event

def homepage(request):
    events = Event.objects.all().order_by('start')
    return render(request, 'homepage.html', {'events': events})

def event_list(request,):
    events = Event.objects.all().order_by('start')
    return render(request, 'events.html', {'events': events})