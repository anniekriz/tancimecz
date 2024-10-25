from django import forms
from .widgets import CustomTimeWidget
from .models import Location, EventGroup, Event, Lector, Workshop

class Search(forms.Form):
   query = forms.CharField(required=False, label='Search')

class Search_lectors(forms.Form):
   query = forms.CharField(required=False, label='Search_lectors')

class EventGroupForm(forms.ModelForm):
    class Meta:
        model = EventGroup
        fields = '__all__'
        widgets = {
            'startTime': CustomTimeWidget(),
            'endTime': CustomTimeWidget(),
        }
