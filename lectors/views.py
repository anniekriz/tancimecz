from django.shortcuts import render
from django.http import HttpResponse
from .models import Lector

# Create your views here.

def lector_list(request):
    lectors = Lector.objects.all()
    return render(request, 'lectors.html', {'lectors': lectors})

def lector_page(request, id):
    # return HttpResponse(id)
    lector = Lector.object.get(id=id)
    return render(request, 'lector_page.html', {'lector': lector})