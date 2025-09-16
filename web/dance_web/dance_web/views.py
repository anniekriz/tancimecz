from django.shortcuts import render, redirect
from danceapp.models import Event, Lector, Workshop, EventLector
from danceapp.forms import Search, Search_lectors
from django.db.models import Q
from django.utils import timezone
from itertools import chain
from django.db.models import Count
from django.utils.timezone import now
from django.core.paginator import Paginator
from collections import OrderedDict
from itertools import chain
from datetime import datetime, date, time as dtime
from django.urls import reverse

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
            'selected_filter': selected_filter,
            "query": "",
            "is_search": False,
        }
    elif selected_filter == 'EVENT':
        combined = Event.objects.all().order_by('date')
        context = {
            'combined': combined,
            'selected_filter': selected_filter,
            "query": "",
            "is_search": False,
        }
    else:
        events = Event.objects.all().order_by('date')
        workshops = Workshop.objects.all().order_by('start')
        combined = list(set(chain(events, workshops)))  # Ensure combined list is unique
        combined.sort(key=lambda x: getattr(x, 'date', getattr(x, 'start', None)))
        context = {
            'combined': combined,
            'selected_filter': selected_filter,
            "query": "",
            "is_search": False,
        }

    return render(request, 'events.html', context)

def past_events(request):
    selected_filter = request.GET.get('filter', 'ALL')
    page_number = request.GET.get('page', 1)
    prev_year = request.GET.get('last_year')
    # Only suppress the first year heading when the request comes from the
    # AJAX loader. When a user navigates directly to a later page we still
    # want to show the year divider, even if ``last_year`` is in the query
    # string.
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        prev_year = int(prev_year) if prev_year else None
    else:
        prev_year = None
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

    page_items = list(page_obj.object_list)
    grouped = OrderedDict()
    for item in page_items:
        year = item.date.year if hasattr(item, 'date') else item.start.year
        grouped.setdefault(year, []).append(item)

    last_year = None
    if page_items:
        last_item = page_items[-1]
        last_year = last_item.date.year if hasattr(last_item, 'date') else last_item.start.year

    context = {
        'grouped_events': grouped,
        'selected_filter': selected_filter,
        'show_past': True,
        'page_obj': page_obj,
        'last_year': last_year,
        'prev_year': prev_year,
        "query": "",
        "is_search": False,
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

from itertools import chain
from datetime import datetime, date, time as dtime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

# ------ pomocné: převod na datetime kvůli řazení ------
def get_start_dt(obj):
    """
    Event -> date (+ parent.startTime pokud je), Workshop -> start (+ startTime)
    Fallbacky drží pořadí i když čas chybí.
    """
    tz = timezone.get_current_timezone()

    # Event
    if hasattr(obj, "date"):
        d = obj.date
        t = None
        if getattr(obj, "parent", None) and getattr(obj.parent, "startTime", None):
            t = obj.parent.startTime
        if not t:
            t = dtime.min
        return timezone.make_aware(datetime.combine(d, t), tz)

    # Workshop
    if hasattr(obj, "start"):
        d = obj.start
        t = getattr(obj, "startTime", None) or dtime.min
        return timezone.make_aware(datetime.combine(d, t), tz)

    # fallback
    return timezone.make_aware(datetime.max, tz)

# ------ pomocné: poskládání "textu" pro hledání ------
def _str_if(v):
    if v is None:
        return ""
    if isinstance(v, (datetime, )):
        return v.strftime("%Y-%m-%d %H:%M")
    if isinstance(v, date):
        return v.strftime("%d.%m.%Y")
    if isinstance(v, dtime):
        return v.strftime("%H:%M")
    return str(v)

def event_haystack(e):
    parts = []

    # samotný Event
    parts.append(_str_if(getattr(e, "description", "")))
    parts.append(_str_if(getattr(e, "date", "")))

    # parent (EventGroup)
    p = getattr(e, "parent", None)
    if p:
        parts.append(_str_if(getattr(p, "description", "")))
        parts.append(_str_if(getattr(p, "startTime", "")))
        parts.append(_str_if(getattr(p, "endTime", "")))

        # location
        loc = getattr(p, "location", None)
        if loc:
            for name in ("town", "name", "street", "address"):
                if hasattr(loc, name):
                    parts.append(_str_if(getattr(loc, name)))

        # lectors (ManyToMany přes through)
        if hasattr(p, "lector"):
            for lec in p.lector.all():
                for name in ("firstName", "lastName", "name"):
                    if hasattr(lec, name):
                        parts.append(_str_if(getattr(lec, name)))

    return " ".join(parts)

def workshop_haystack(w):
    parts = [
        _str_if(getattr(w, "title", "")),
        _str_if(getattr(w, "title2", "")),
        _str_if(getattr(w, "description", "")),
        _str_if(getattr(w, "price", "")),
        _str_if(getattr(w, "start", "")),
        _str_if(getattr(w, "end", "")),
        _str_if(getattr(w, "startTime", "")),
        _str_if(getattr(w, "endTime", "")),
    ]
    loc = getattr(w, "location", None)
    if loc:
        for name in ("town", "name", "street", "address"):
            if hasattr(loc, name):
                parts.append(_str_if(getattr(loc, name)))

    if hasattr(w, "lector"):
        for lec in w.lector.all():
            for name in ("firstName", "lastName", "name"):
                if hasattr(lec, name):
                    parts.append(_str_if(getattr(lec, name)))

    return " ".join(parts)

def contains_casefold(haystack: str, needle: str) -> bool:
    return needle.casefold() in haystack.casefold()


# ------ samotné vyhledávání ------
from django.db.models import Prefetch
# importuj si Event, Workshop, Lector, Location

def search_result(request):
    query = (request.GET.get("query") or "").strip()
    selected_filter = (request.GET.get("filter") or "ALL").upper()
    show_past = request.GET.get("show_past") == "1"

    # prázdný dotaz -> zpět na normální stránku (zachovej filtr)
    if not query:
        url = reverse("past_events" if show_past else "events")
        return redirect(f"{url}?filter={selected_filter}") if selected_filter and selected_filter != "ALL" else redirect(url)

    today = timezone.localdate()

    # ---- Eventy ----
    e_qs = Event.objects.select_related("parent", "parent__location") \
                        .prefetch_related("parent__lector")
    e_qs = e_qs.filter(date__lt=today).order_by("-date") if show_past else e_qs.filter(date__gte=today).order_by("date")

    # ---- Workshopy ----
    w_qs = Workshop.objects.select_related("location").prefetch_related("lector")
    w_qs = w_qs.filter(end__lt=today).order_by("-start") if show_past else w_qs.filter(start__gte=today).order_by("start")

    # respektuj přepínač typu
    if selected_filter == "EVENT":
        w_qs = Workshop.objects.none()
    elif selected_filter == "WORKSHOP":
        e_qs = Event.objects.none()

    # Pythoní fulltext přes všechny relevantní atributy (case-insensitive)
    events_list = [e for e in e_qs if contains_casefold(event_haystack(e), query)]
    workshops_list = [w for w in w_qs if contains_casefold(workshop_haystack(w), query)]

    # smíchat + seřadit jako na hlavní stránce
    combined = events_list + workshops_list
    combined.sort(key=get_start_dt, reverse=show_past)

    return render(request, "events.html", {
        "is_search": True,
        "query": query,
        "combined": combined,
        "selected_filter": selected_filter,
        "show_past": show_past,
    })

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
