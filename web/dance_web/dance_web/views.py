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
        combined = Workshop.objects.all().order_by('start')
        context = {
            'combined': combined,
            'selected_filter': selected_filter
        }
    elif selected_filter == 'EVENT':
        combined = Event.objects.all().order_by('date')
        context = {
            'combined': combined,
            'selected_filter': selected_filter
        }
    else:
        events = Event.objects.all().order_by('date')
        workshops = Workshop.objects.all().order_by('start')
        combined = list(set(chain(events, workshops)))  # Ensure combined list is unique
        combined.sort(key=lambda x: getattr(x, 'date', getattr(x, 'start', None)))
        context = {
            'workshops': workshops,
            'events': events,
            'combined': combined,
            'selected_filter': selected_filter
        }

    return render(request, 'events.html', context)

def past_events(request):
    now = timezone.now().date()
    past_events = Event.objects.filter(date__lt=now)
    past_workshops = Workshop.objects.filter(end__lt=now)
    
    combined = list(past_events) + list(past_workshops)
    
    context = {
        'combined': combined,
    }
    return render(request, 'past_events.html', context)

def lector_list(request):
    lectors = Lector.objects.all().order_by()
    return render(request, 'lectors.html', {'lectors': lectors})

def lector_page(request, slug):
    lectors = Lector.objects.all().order_by('id')
    lector = Lector.objects.get(slug=slug)
    lector_index = list(lectors).index(lector)
    prev_lector = lectors[lector_index - 1] if lector_index > 0 else None
    next_lector = lectors[lector_index + 1] if lector_index < len(lectors) - 1 else None
    events = Event.objects.filter(parent__lector=lector).order_by('date')
    workshops = Workshop.objects.filter(lector=lector).order_by('start')
    combined = sorted(chain(events, workshops), key=lambda x: x.date if hasattr(x, 'date') else x.start)
    context = {
        'workshops': workshops,
        'events': events,
        'combined': combined,
        'lector': lector,
        'prev_lector': prev_lector,
        'next_lector': next_lector,
    }
    return render(request, 'lector_page.html', context)

def evening_page(request, id):
    events = Event.objects.all().order_by('date')
    event = Event.objects.get(id=id)
    lectors = Lector.objects.all()
    
    context = {
        'events': events,
        'event': event,
        'lectors': lectors
    }
    return render(request, 'evening_page.html', context)

def workshop_page(request, id):
    workshops = Workshop.objects.all().order_by('start')
    workshop = Workshop.objects.get(id=id)
    lectors = Lector.objects.all()
    
    context = {
        'events': workshops,
        'event': workshop,
        'lectors': lectors
    }
    return render(request, 'workshop_page.html', context)

def search_result(request):
    form = Search(request.GET)
    events = Event.objects.all()
    workshops = Workshop.objects.all()

    if 'query' in request.GET:
        if form.is_valid():
            query = form.cleaned_data.get('query')
            events = Event.objects.filter(
                Q(parent__description__icontains=query) |
                Q(parent__lector__firstName__icontains=query) |
                Q(parent__lector__lastName__icontains=query) |
                Q(parent__location__town__icontains=query)
            ).distinct()
            workshops = Workshop.objects.filter(
                Q(title__icontains=query) |
                Q(lector__firstName__icontains=query) |
                Q(lector__lastName__icontains=query) |
                Q(description__icontains=query) |
                Q(location__town__icontains=query)
            ).distinct()

    return render(request, 'events.html', {'form': form, 'events': events, 'workshops': workshops})

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
