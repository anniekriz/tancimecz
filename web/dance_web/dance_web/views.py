from django.shortcuts import render
from danceapp.models import Event, Lector, Workshop, EventLector
from danceapp.forms import Search, Search_lectors
from django.db.models import Q
from django.utils import timezone
from itertools import chain
from django.db.models import Count
from django.utils.timezone import now
from django.core.paginator import Paginator

ludmila_id = 25

future_events_filter = Q(eventgroup__event__date__gte=now().date())
future_workshops_filter = Q(workshop__start__gte=now().date())

def homepage(request):
    events = Event.objects.all().order_by('date')
    workshops = Workshop.objects.all().order_by('start')
    lectors = Lector.objects.annotate(event_count=Count('eventgroup__event', filter=future_events_filter, distinct=True) + Count('workshop', filter=future_workshops_filter, distinct=True)*2).exclude(id=ludmila_id).order_by('-event_count', 'lastName', 'firstName')

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
            'combined': combined,
            'selected_filter': selected_filter
        }

    return render(request, 'events.html', context)

def past_events(request):
    selected_filter = request.GET.get('filter', 'ALL')
    page_number = request.GET.get('page', 1)
    today = timezone.now().date()

    if selected_filter == 'WORKSHOP':
        items = Workshop.objects.filter(end__lt=today).order_by('-start')
    elif selected_filter == 'EVENT':
        items = Event.objects.filter(date__lt=today).order_by('-date')
    else:
        events = Event.objects.filter(date__lt=today).order_by('-date')
        workshops = Workshop.objects.filter(end__lt=today).order_by('-start')
        items = list(chain(events, workshops))
        items.sort(key=lambda x: getattr(x, 'date', getattr(x, 'start', None)), reverse=True)

    paginator = Paginator(items, 20)  # show 20 items per page
    page_obj = paginator.get_page(page_number)

    context = {
        'combined': page_obj.object_list,
        'selected_filter': selected_filter,
        'show_past': True,
        'page_obj': page_obj,
    } 
    
    return render(request, 'events.html', context)

def lector_list(request):
    lectors = Lector.objects.all().exclude(id=ludmila_id).order_by('lastName','firstName')
    lector_ludmila = Lector.objects.all().filter(id=ludmila_id).first()    
    return render(request, 'lectors.html', {"lector_ludmila": lector_ludmila, "lectors": lectors})

def lector_page(request, slug):
    lectors = Lector.objects.all().order_by('id')
    lector = Lector.objects.get(slug=slug)
    lector_index = list(lectors).index(lector)
    prev_lector = lectors[lector_index - 1] if lector_index > 0 else None
    next_lector = lectors[lector_index + 1] if lector_index < len(lectors) - 1 else None
    events = Event.objects.filter(parent__lector=lector)
    workshops = Workshop.objects.filter(lector=lector)
    combined = list(set(chain(events, workshops)))  # Ensure combined list is unique
    combined.sort(key=lambda x: getattr(x, 'date', getattr(x, 'start', None)))
    context = {
        'combined': combined,
        'lector': lector,
        'prev_lector': prev_lector,
        'next_lector': next_lector,
    }
    return render(request, 'lector_page.html', context)

def evening_page(request, id):
    event = Event.objects.get(id=id)
    # event_group = event.parent
    # event_lectors = EventLector.objects.filter(eventId=event_group).order_by('order')
    # lectors = [event_lector.lectorId for event_lector in event_lectors]  # Extract Lector objects from EventLector
    
    context = {
        'event': event,
        # 'lectors': lectors,
    }
    return render(request, 'evening_page.html', context)

def workshop_page(request, id):
    workshop = Workshop.objects.get(id=id)
    
    context = {
        'event': workshop,
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
