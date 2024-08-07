from django.shortcuts import render
from danceapp.models import Event, Lector, Workshop
from danceapp.forms import Search, Search_lectors
from django.db.models import Q
from django.utils import timezone
from itertools import chain
from django.http import JsonResponse
from django.template.loader import render_to_string

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
        combined = list(set(chain(events, workshops)))  # Ensure combined list is unique
        combined.sort(key=lambda x: x.date if hasattr(x, 'date') else x.start)
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
    form = Search(request.GET or None)
    events = Event.objects.all()
    workshops = Workshop.objects.all()

    if 'query' in request.GET and form.is_valid():
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

        if request.is_ajax():
            combined_results = list(events) + list(workshops)
            results_html = '<div class="events">'
            for item in combined_results:
                if isinstance(item, Event):
                    results_html += f"""
                    <div class="event">
                        <h2 class="event-title">{item.parent.location.town}</h2>
                        <div class="event-image">
                            <img src="{item.parent.image.url if item.parent.image else ''}">
                        </div>
                        <div class="event-details">
                            <div class="event-date">
                                <p>{item.date.strftime('%d.%m.%Y')} {item.parent.startTime.strftime('%H:%M')} - {item.parent.endTime.strftime('%H:%M') if item.parent.endTime else 'N/A'}</p>
                            </div>
                            <div class="event-location">
                                <p><strong>Kde: </strong>{item.parent.location.name} {item.parent.location.address}, {item.parent.location.town}</p>
                            </div>
                            <div class="event-lector">
                                <p><strong>S kým: </strong>{", ".join([f'<a href="#">' + lector.firstName + ' ' + lector.lastName + '</a>' for lector in item.parent.lector.all()])}</p>
                            </div>
                            <div class="event-description">
                                <p class="description"><strong>Na co se těšit: </strong>{item.parent.description}<br>{item.description}</p>
                            </div>
                        </div>
                    </div>
                    """
                elif isinstance(item, Workshop):
                    results_html += f"""
                    <div class="workshop">
                        <h2 class="workshop-title">{item.title}</h2>
                        <div class="workshop-image">
                            <img src="{item.image.url if item.image else ''}">
                        </div>
                        <div class="workshop-details">
                            <div class="workshop-date">
                                <p>{item.start.strftime('%d.%m.%Y')} - {item.end.strftime('%d.%m.%Y')}</p>
                            </div>
                            <div class="workshop-location">
                                <p><strong>Kde: </strong>{item.location.name} {item.location.address}, {item.location.town}</p>
                            </div>
                            <div class="workshop-lector">
                                <p><strong>S kým: </strong>{", ".join([f'<a href="#">' + lector.firstName + ' ' + lector.lastName + '</a>' for lector in item.lector.all()])}</p>
                            </div>
                            <div class="workshop-description">
                                <p class="description"><strong>Na co se těšit: </strong>{item.description}</p>
                            </div>
                        </div>
                    </div>
                    """
            results_html += '</div>'
            return JsonResponse({'results_html': results_html}, safe=False)

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
