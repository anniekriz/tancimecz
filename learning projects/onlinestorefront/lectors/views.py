from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Lector
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.shortcuts import reverse
from django.views.generic import TemplateView, FormView

# Create your views here.

def lector_list(request):
    lectors = Lector.objects.all()
    return render(request, 'lectors.html', {'lectors': lectors})

def lector_page(request, id):
    # return HttpResponse(id)
    lector = Lector.objects.get(id=id)
    return render(request, 'lector_page.html', {'lector': lector})

class SuccessView(TemplateView):
    template_name = "success.html"

class ContactView(FormView):
    form_class = ContactForm
    template_name = "contact.html"

    def get_success_url(self):
        return reverse("contact")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")

        full_message = f"""
            Received message below from {email}, {subject}
            ________________________


            {message}
            """
        send_mail(
            subject="Received contact form submission",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL],
        )
        return super(ContactView, self).form_valid(form)
    