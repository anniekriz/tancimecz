from django import forms

class Search(forms.Form):
   query = forms.CharField(required=False, label='Search')

class Search_lectors(forms.Form):
   query = forms.CharField(required=False, label='Search_lectors')