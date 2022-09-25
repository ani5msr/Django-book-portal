from django.urls import path,include
from django.views.generic import TemplateView
from main import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
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
 path('admin/', admin.site.urls),
 path('', include('main.urls')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)