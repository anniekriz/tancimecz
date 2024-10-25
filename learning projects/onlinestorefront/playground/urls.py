#map our urls for our view functions

from django.urls import path
from . import views

# array of url pattern objects
# URL configuration (URLconf module)
urlpatterns = [
    # "playground/hello" is what we are gonna type in the url to call this function, because we added the playground/ to the main URLconf module, we can use only hello/ in the handler
    path('hello/', views.say_hello)
]