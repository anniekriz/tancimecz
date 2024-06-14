from django.shortcuts import render
from danceapp.models import Event
from danceapp.forms import Search
from django.db.models import Q

def homepage(request):
    events = Event.objects.all().order_by('start')
    return render(request, 'homepage.html', {'events': events})

def event_list(request):
    events = Event.objects.all().order_by('start')
    return render(request, 'events.html', {'events': events})

def search_result(request):
    form = Search(request.GET)
    events = Event.objects.all()

    if 'query' in request.GET:
        if form.is_valid():
            query = form.cleaned_data.get('query')
            events = Event.objects.filter(
                Q(title__icontains=query) |
                Q(lector__icontains=query) |
                Q(description__icontains=query) |
                Q(location__town__icontains=query)
            )

    return render(request, 'events.html', {'form': form, 'events': events})