from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from guestbookapp.models import Entry

# Create your tests here.
class GuestbookTests(TestCase):
    def setUp(self):
        #Create test user for tests
        self.test_user = User.objects.create_user(username="test_user", password="testpassword")
        self.client = Client()

### TESTS FOR LANDING VIEW ###
    def test_landing_view_unauthenticated(self):
        """Opens the login page, when unauthenticated"""
        #Log out any existing user
        self.client.logout()
        #GET request to the landing page
        response = self.client.get(reverse("landing"))
        #Status code OK
        self.assertEqual(response.status_code, 200)
        #Has the correct template
        self.assertTemplateUsed(response, "guestbookapp/login.html")
        #Sends the context message to log in first
        self.assertContains(response, "Please log in first")
    
    def test_landing_view_authenticated(self):
        """Open the guestbook page, when authenticated"""
        #Login with test_user
        self.client.login(username="test_user", password="testpassword")
        #GET request to the landing page
        response = self.client.get(reverse("landing"))
        #Check that redirection works
        self.assertRedirects(response, reverse("guestbookview"))

### TESTS FOR LOGINVIEW ###

    def test_login_view_valid_credentials(self):
        """Redirects to guestbook page, when valid credentials given"""
        #Log out any existing user
        self.client.logout()
        #Credentials for the post request
        data = {"username": "test_user", "pwd": "testpassword"}
        #POST request to the login page
        response = self.client.post(reverse("loginview"), data)
        #Check that redirection works
        self.assertRedirects(response, reverse("guestbookview"))
        #Check that the user is authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_invalid_credentials(self):
        """Opens the login page again, with error message, when invalid credentials given"""
        #Log out any existing user
        self.client.logout()
        #Invalid credentials for the post request
        data = {"username": "foo", "pwd": "bar"}
        #POST request to the login page
        response = self.client.post(reverse("loginview"), data)
        #Check that login page opens
        self.assertTemplateUsed(response, "guestbookapp/login.html")
        #Check the error message
        self.assertContains(response, "Invalid username or password")
        #Check status code OK
        self.assertEqual(response.status_code, 200)

    def test_login_view_get_request(self):
        """Opens the login page when get request made"""
        #Log out any existing user
        self.client.logout()
        #GET request to the login page
        response = self.client.get(reverse("loginview"))
        #Check that correct template used
        self.assertTemplateUsed(response, "guestbookapp/login.html")
        #Status code OK
        self.assertEqual(response.status_code, 200)

### TESTS FOR LOGOUTVIEW ###
    
    def test_logout_view_post(self):
        """POST request signs out and returns to login page"""
        #Log in first
        self.client.login(username="test_user", password="testpassword")
        #POST request to logout page
        response = self.client.post(reverse("logoutview"))
        #Check for correct template
        self.assertTemplateUsed(response, "guestbookapp/login.html")
        #Check for successful logout message
        self.assertContains(response, "Successfully logged out")
        #Check that no user is authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        #Status code OK
        self.assertEqual(response.status_code, 200)

    def test_logout_view_get(self):
        """GET request opens the guestbookview when authenticated. This ends up in log in view, if not authenticated"""
        #Log in first
        self.client.login(username="test_user", password="testpassword")
        #GET response to logout page
        response = self.client.get(reverse("logoutview"))
        #Check for sueccessful redirection
        self.assertRedirects(response, reverse("guestbookview"))
        #Sign out to test the redirect when not authenticated
        self.client.logout()
        #GET response to logout page
        response = self.client.get(reverse("logoutview"))
        #Status code OK
        self.assertEqual(response.status_code, 302)

### TESTS FOR GUESTBOOKVIEW ###
    
    def test_guestbook_view_authenticated(self):
        """GET request to /guestbook route when authenticated"""
        #Log in first
        self.client.login(username="test_user", password="testpassword")
        #GET request to guestbook route
        response = self.client.get(reverse("guestbookview"))
        #Check correct template
        self.assertTemplateUsed(response, "guestbookapp/guestbook.html")
        #Check status code
        self.assertEqual(response.status_code, 200)
    
    def test_guestbook_view_not_authenticated(self):
        """GET request to /guestbook route when not authenticated"""
        #Log out any user
        self.client.logout()
        #GET request to guestbook route
        response = self.client.get(reverse("guestbookview"))
        #Check for correct redirect
        self.assertRedirects(response, reverse("loginview"))

### TESTS FOR CREATE ENTRY VIEW ###
    
    def test_creating_valid_entry(self):
        """Valid POST request for entry creation"""
        #Log in first
        self.client.login(username="test_user", password="testpassword")
        #Remove any similar entry first
        Entry.objects.filter(entry_text="foo", author ="bar").delete()
        #Data for entry
        data = {"entry_text": "foo", "author": "bar"}
        #POST request
        self.client.post(reverse("create"), data)
        #Check that entry is found
        created_user = Entry.objects.filter(entry_text="foo", author ="bar").exists()
        self.assertTrue(created_user)

    def test_creating_invalid_entry(self):
        """Invalid POST request with missing mandatory value"""
        #Log in first
        self.client.login(username="test_user", password="testpassword")
        #Empty data for entry
        data = {"entry_text": "", "author": ""}
        #POST request
        response = self.client.post(reverse("create"), data)
        #Check it re-opens the create view
        self.assertTemplateUsed(response, "guestbookapp/create.html")
        #Check for error message
        self.assertContains(response, "Please fill in mandatory fields: text and author")
        #Status code OK
        self.assertEqual(response.status_code, 200)
    
    def test_create_view_get_authenticated(self):
        """Test opening the create view with a get request, when authenticated"""
        #Log in first
        self.client.login(username="test_user", password="testpassword")
        #GET request
        response = self.client.get(reverse("create"))
        #Check template
        self.assertTemplateUsed(response, "guestbookapp/create.html")
        #Status code OK
        self.assertEqual(response.status_code, 200)
    
    def test_create_view_get_not_authenticated(self):
        """Test opening the create view with a get request, when not authenticated. Sends to login page with message"""
        #Log out any user first
        self.client.logout()
        #GET request
        response = self.client.get(reverse("create"))
        #Check template
        self.assertTemplateUsed(response, "guestbookapp/login.html")
        #Check for error message
        self.assertContains(response, "Please log in first")