from django.urls import path,include
from django.views.generic import TemplateView
from main import views
from django.contrib import admin
urlpatterns = [
 path(
 "about-us/",
 TemplateView.as_view(template_name="aboutUsPage.html"),
 name="about_us",
 ),
 path(
 "",
 TemplateView.as_view(template_name="home.html"),
 name="home",
 ),
 path(
 "contact-us/",
 views.ContactUsView.as_view(),
 name="contact_us",
 ),
 path(
 "products/<slug:tag>/",
 views.ProductListView.as_view(),
 name="products",
 ),
]  