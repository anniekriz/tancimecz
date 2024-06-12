from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Váš e-mail"})
    )
    subject = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Předmět"}))
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Zpráva"})
    )