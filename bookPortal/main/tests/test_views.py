from django.test import TestCase
from django.urls import reverse
from main import forms
class TestPage(TestCase):
 def test_home_page_works(self):
    response = self.client.get(reverse("home"))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'home.html')
    self.assertContains(response, 'Book Portal')
 def test_about_us_page_works(self):
    response = self.client.get(reverse("about_us"))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'aboutUsPage.html')
    self.assertContains(response, 'Book Portal')
 def test_contact_us_page_works(self):
    response = self.client.get(reverse("contact_us"))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'main/contactForm.html')
    self.assertContains(response, 'Book Portal')
    self.assertIsInstance(
    response.context["form"], forms.ContactForm)