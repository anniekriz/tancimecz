from django.shortcuts import render
from danceapp.models import Event, Lector, EventType
from danceapp.forms import Search, Search_lectors
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
    event_type = request.GET.get('type', 'ALL')
    if event_type == 'ALL':
        events = Event.objects.all().order_by('start')
    elif event_type == 'EVENT':
        events = Event.objects.filter(type=EventType.EVENT).order_by('start')
    elif event_type == 'WORKSHOP':
        events = Event.objects.filter(type=EventType.WORKSHOP).order_by('start')
    else:
        events = Event.objects.all().order_by('start')

    context = {
        'events': events,
        'EventType': EventType,
        'selected_type': event_type,  
    }
    return render(request, 'events.html', context)

def lector_list(request):
    lectors = Lector.objects.all().order_by()
    return render(request, 'lectors.html', {'lectors': lectors})

def lector_page(request, slug):
    lector = Lector.objects.get(slug=slug)
    events = Event.objects.filter(lector=lector).order_by('start')
    context = {
        'events': events,
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
                Q(firstName__icontains=query) |
                Q(description__icontains=query) 
            )

    return render(request, 'lectors.html', {'form': form, 'lectors': lectors})

def o_tancich(request):
    return render(request,'o_tancich.html')

def o_nas(request):
    return render(request,'o_nas.html')