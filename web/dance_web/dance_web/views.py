from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')

def event_list(request):
    return render(request, 'events.html')