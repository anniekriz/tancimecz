from django.shortcuts import render
from danceapp.models import Event, Lector
from danceapp.forms import Search
from django.db.models import Q

def homepage(request):
    events = Event.objects.all().order_by('start')
    lectors = Lector.objects.all()
    context = {
        'events': events,
        'lectors': lectors
    }
    return render(request, 'homepage.html', context)

def event_list(request):
    events = Event.objects.all().order_by('start')
    return render(request, 'events.html', {'events': events})

def lector_page(request, slug):
    lector = Lector.objects.get(slug=slug)
    return render(request, 'lector_page.html', {'lector': lector})

def search_result(request):
    form = Search(request.GET)
    events = Event.objects.all()

    if 'query' in request.GET:
        if form.is_valid():
            query = form.cleaned_data.get('query')
            events = Event.objects.filter(
                Q(title__icontains=query) |
                Q(lector__firstName__icontains=query) |
                Q(lector__lastName__icontains=query) |
                Q(description__icontains=query) |
                Q(location__town__icontains=query)
            )

    return render(request, 'events.html', {'form': form, 'events': events})