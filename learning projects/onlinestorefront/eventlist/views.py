from django.shortcuts import render
from django.http import HttpResponse
from .models import Event
from .forms import Search
from django.db.models import Q

# Create your views here.

def event_list(request):
    events = Event.objects.all().order_by('date_time')
    return render(request, 'eventlist.html', {'events': events})

def search_result(request):
    form = Search(request.GET)
    events = Event.objects.all()

    if 'query' in request.GET:
        if form.is_valid():
            query = form.cleaned_data.get('query')
            events = Event.objects.filter(
                Q(title__icontains=query) |
                Q(lector__icontains=query) |
                Q(town__icontains=query)
            )

    return render(request, 'search_result.html', {'form': form, 'events': events})