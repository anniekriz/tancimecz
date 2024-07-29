from django.shortcuts import render
from danceapp.models import Event, Lector, Workshop
from danceapp.forms import Search, Search_lectors
from django.db.models import Q
from django.utils import timezone
from itertools import chain

def homepage(request):
    events = Event.objects.all().order_by('date')
    workshops = Workshop.objects.all().order_by('start')
    lectors = Lector.objects.all()
    
    context = {
        'events': events,
        'lectors': lectors,
        'workshops': workshops, 
    }
    return render(request, 'homepage.html', context)

def event_list(request):
    selected_filter = request.GET.get('filter', 'ALL')
    if selected_filter == 'WORKSHOP':
        workshops = Workshop.objects.all().order_by('start')
        context = {
            'workshops': workshops,
            'events': [],
            'selected_filter': selected_filter
        }
    elif selected_filter == 'EVENT':
        events = Event.objects.all().order_by('date')
        context = {
            'workshops': [],
            'events': events,
            'selected_filter': selected_filter
        }
    else:
        events = Event.objects.all().order_by('date')
        workshops = Workshop.objects.all().order_by('start')
        combined = sorted(chain(events, workshops), key=lambda x: x.date if hasattr(x, 'date') else x.start)
        context = {
            'workshops': workshops,
            'events': events,
            'combined': combined,
            'selected_filter': selected_filter
        }

    return render(request, 'events.html', context)

def past_events(request):
    now = timezone.now()
    past_events_events = Event.objects.filter(date__lt=now.date()).order_by('-date')
    past_workshops = Workshop.objects.filter(end__lt=now).order_by('-end')
    
    context = {
        'past_events': past_events_events,
        'past_workshops': past_workshops,
        'selected_type': 'PAST'
    }
    return render(request, 'past_events.html', context)

def lector_list(request):
    lectors = Lector.objects.all().order_by()
    return render(request, 'lectors.html', {'lectors': lectors})

def lector_page(request, slug):
    lector = Lector.objects.get(slug=slug)
    events = Event.objects.all().order_by('date')
    workshops = Workshop.objects.all().order_by('start')
    combined = sorted(chain(events, workshops), key=lambda x: x.date if hasattr(x, 'date') else x.start)
    context = {
        'workshops': workshops,
        'events': events,
        'combined': combined,
        'lector': lector
    }
    return render(request, 'lector_page.html', context)

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

def search_result_lectors(request):
    form = Search_lectors(request.GET)
    lectors = Lector.objects.all()

    if 'query' in request.GET:
        if form.is_valid():
            query = form.cleaned_data.get('query')
            lectors = Lector.objects.filter(
                Q(firstName__icontains=query) |
                Q(lastName__icontains=query) |
                Q(description__icontains=query)
            )

    return render(request, 'lectors.html', {'form': form, 'lectors': lectors})

def o_tancich(request):
    return render(request,'o_tancich.html')

def o_nas(request):
    return render(request,'o_nas.html')
