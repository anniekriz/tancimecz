from django.shortcuts import render
from danceapp.models import Event, Lector, Workshop
from danceapp.forms import Search, Search_lectors
from django.db.models import Q
from django.utils import timezone
from itertools import chain
import requests
from datetime import datetime
from django.http import JsonResponse

import logging

# Konfigurace loggeru
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
        workshops = get_all_workshops()
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
        workshops = get_all_workshops()
        combined = sorted(chain(events, workshops), key=lambda x: x.date if hasattr(x, 'date') else x['start'])
        context = {
            'workshops': workshops,
            'events': events,
            'combined': combined,
            'selected_filter': selected_filter
        }

    return render(request, 'events.html', context)

#sosání ací z Nesměně 

def fetch_nesmen_events():
    api_url1 = "https://www.centrum-nesmen.cz/LocationService/GetLocationList?format=json"
    response1 = requests.get(api_url1)
    api_url2 = "https://www.centrum-nesmen.cz/CourseService/GetCourseList?count=4&type=Dances&language=CZ&includeImages=true&format=json"
    response2 = requests.get(api_url2)
    locations = response1.json().get('list', [])
    courses = response2.json().get('list', [])
    workshops = []
    workshop = {
        'title': "Pokusnej workshop :)",
        'start': datetime.strptime("2024-10-01", "%Y-%m-%d").date(),
        'end': datetime.strptime("2024-10-03", "%Y-%m-%d").date(),
        'image': ""
    }
    workshops.append(workshop)

   #for course in courses:
   #    workshop = {
   #        'title': course['name'],
   #        'start': datetime.strptime(course['startDate'], "%Y-%m-%d").date(),
   #        'end': datetime.strptime(course['endDate'], "%Y-%m-%d").date(),
   #        'image': course.get('image', '')
   #    }
   #    workshops.append(workshop)

    return workshops

def get_all_workshops():
    db_workshops = list(Workshop.objects.all().values('title', 'start', 'end', 'image'))
    external_workshops = fetch_nesmen_events()
    
    # Combine the lists
    all_workshops = db_workshops + external_workshops
    
    # Sort the combined list by 'start'
    all_workshops_sorted = sorted(all_workshops, key=lambda x: x['start'])
    
    return all_workshops_sorted



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
    lector = Lector.objects.get(slug=slug)
    events = Event.objects.filter(parent__lector=lector).order_by('date')
    workshops = Workshop.objects.filter(lector=lector).order_by('start')
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
