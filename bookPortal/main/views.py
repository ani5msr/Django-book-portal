from django.shortcuts import render
# Create your views here.
from django.views.generic.edit import FormView
from main import forms
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from main import models
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, CreateView,UpdateView, DeleteView
from django.views.generic.edit import (
 FormView,
 CreateView,
 UpdateView,
 DeleteView,
)
logger = logging.getLogger(__name__)
class ContactUsView(FormView):
    template_name = "contactForm.html"
    form_class = forms.ContactForm
    success_url = "/"
    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)
class ProductListView(ListView):
    template_name = "main/productList.html"
    paginate_by = 4
    def get_queryset(self):
        tag = self.kwargs['tag']
        self.tag = None
        if tag != "all":
            self.tag = get_object_or_404(models.ProductTag, slug=tag)
        if self.tag:
            products = models.Product.objects.active().filter(tags=self.tag)
        else:
            products = models.Product.objects.active()
        return products.order_by("name")
class SignupView(FormView):
    template_name = "signUp.html"
    form_class = forms.UserCreationForm
    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to
    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        logger.info("New signup for email=%s through SignupView", email)
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        form.send_mail()
        messages.info(self.request, "You signed up successfully.")
        return response
class AddressListView(LoginRequiredMixin, ListView):
    model = models.Address
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
class AddressCreateView(LoginRequiredMixin, CreateView):
    model = models.Address
    fields = ["name","address1","address2","zip_code","city","country",]
    success_url = reverse_lazy("address_list")
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)
class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Address
    fields = ["name","address1","address2","zip_code","city","country",]
    success_url = reverse_lazy("address_list")
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Address
    success_url = reverse_lazy("address_list")
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
def add_to_cart(request):
 product = get_object_or_404(models.Product, pk=request.GET.get("product_id"))
 cart= request.cart
 if not request.cart:
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
        cart = models.cart.objects.create(user=user)
        request.session["cart_id"] = cart.id
    cartline, created = models.cartLine.objects.get_or_create(cart=cart, product=product)
    if not created:
        cartline.quantity += 1
        cartline.save()
 return HttpResponseRedirect(reverse("product", args=(product.slug,)))
def manage_cart(request):
 if not request.cart:
    return render(request, "cart.html", {"formset": None})
 if request.method == "POST":
    formset = forms.cartLineFormSet(request.POST, instance=request.cart)
 if formset.is_valid():
    formset.save()
 else:
    formset = forms.cartLineFormSet(instance=request.cart)
 if request.cart.is_empty():
    return render(request, "cart.html", {"formset": None})
 return render(request, "cart.html", {"formset": formset})