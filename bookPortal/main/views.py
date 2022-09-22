from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import FormView
from main import forms
class ContactUsView(FormView):
    template_name = "contactForm.html"
    form_class = forms.ContactForm
    success_url = "/"
    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)