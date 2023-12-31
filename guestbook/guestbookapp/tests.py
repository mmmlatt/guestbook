from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from guestbookapp.models import Entry

# Create your tests here.
class GuestbookTests(TestCase):
    def setUp(self):
        #Create test user for tests
        test_user = User.objects.create(username="test_user")
        test_user.set_password("testpassword")
        test_user.save()
    def test_landing_view_unauthenticated(self):
        """Opens the login page, when unauthenticated"""
        #GET request to the landing page
        response = self.client.get(reverse("landing"))
        #Status code OK
        self.assertEqual(response.status_code, 200)
        #Has the correct template
        self.assertTemplateUsed(response, "guestbookapp/login.html")
        #Sends the context message to log in first
        self.assertContains(response, "Please log in first")