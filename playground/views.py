from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# using HttpResponse
# def say_hello(request):
   # return HttpResponse('Hello World')

# using render
def say_hello(request):
    return render(request, 'hello.html')