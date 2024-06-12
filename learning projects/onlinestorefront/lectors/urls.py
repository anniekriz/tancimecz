from django.urls import path, re_path
from django.conf.urls import url
from . import views
from .views import SuccessView, ContactView

app_name = 'lectors'

urlpatterns = [
    path('', views.lector_list, name="list"),
    # (r'^(?P<name>[\w-]+)/$' mi udělá ze jména lectora url, která bude srozumitelná pro program (na to nejde použít path, musim re_path)
    # \w = všechna písmena, malá i velká, čísla a _, - = i pomlčky, + = neomezená délka
    # name je pouze názav variable, nemusí to být name, je to jedno a do téhle variable, je uložena tak url adresa
    re_path(r'^(?P<id>[\w-]+)/', views.lector_page, name="page"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("success/", SuccessView.as_view(), name="success")
]