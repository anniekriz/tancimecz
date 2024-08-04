from django import forms
from .widgets import CustomTimeWidget
from .widgets import CustomTimeWidget
from django.core.exceptions import ValidationError
import re
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

    def clean_startTime(self):
        start_time = self.cleaned_data.get('startTime')
        if not self.is_valid_time(start_time):
            raise ValidationError('Zadejte čas ve formátu 18, 18:00 nebo 18:00:00.')
        return start_time

    def clean_endTime(self):
        end_time = self.cleaned_data.get('endTime')
        if not self.is_valid_time(end_time):
            raise ValidationError('Zadejte čas ve formátu 18, 18:00 nebo 18:00:00.')
        return end_time

    def is_valid_time(self, time_str):
        pattern = re.compile(r'^\d{1,2}(:\d{2}(:\d{2})?)?$')
        return pattern.match(str(time_str)) is not None