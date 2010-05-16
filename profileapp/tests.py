"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.conf import settings
from profileapp.models import LogDB

class ProfileAppTest(TestCase):
    """ Tests for profileapp application """
    def test_basic_get (self):
        """ Tests, that main page and profiles are accessible """

        # Test access to root page
        self.assertEqual(self.client.get('/').status_code, 200,
                "Main page unreachable")

        # Test access to profile and trailing slash appending
        response = self.client.get('/igor', follow=True)
        self.assertRedirects(response, '/igor/', 301, 200)

    def test_log_middleware (self):
        """ Tests log middleware\
        Each request is logged into LogDB table with HR label\
        This test checks that number of log entries is incremented
        """

        hr_count_before = LogDB.objects.filter(event_type='HR').count()
        self.client.get('/')
        hr_count_after = LogDB.objects.filter(event_type='HR').count()
        self.assertTrue(hr_count_after > hr_count_before,
                "Log middleware doesn't log HTTP Requests")

    def test_login_module (self):
        """ Tests that profile edit page is not accessible by\
        unauthorized users. It should redirect to login page
        """
        self.client.logout()

        # Unauthorized users are redirected to login page
        response = self.client.get('/edit/igor/', follow=True)
        self.assertRedirects(response, '/profile/login/?next=/edit/igor/',
                status_code=302, target_status_code=200)

        # Login page must show page on GET request and authentificate user
        # on POST request
        self.assertEqual(self.client.get("/profile/login/?next=/edit/igor/").\
                status_code, 200)
        # Wrong user
        response = self.client.post('/profile/login/',
                {'username':'someone', 'password':'123', 'next':'/edit/igor/'})
        self.assertEqual(response.status_code, 200,
                "Failure when provide incorrect user credentials")
        response = self.client.post('/profile/login/',
                {'username':'igor', 'password':'123', 'next':'/edit/igor/'})
        self.assertEqual(response.status_code, 302,
                "Successful login did not redirect user")
        self.assertEqual(response['Location'], 'http://testserver/edit/igor/',
                "Wrong redirect target after login")

        # Now user can edit his profile
        # IMPORTANT
        # There is a bug with Django test client and Python 2.6.5 or higher
        # http://groups.google.com/group/django-users/browse_thread/thread/703b2e477d157f66/44e0cc61bf9e0b00?pli=1
        # Test client has some problems with cookies so all requests are
        # done from unauthorized user
        #
        # I passed this test using Python 2.5.1, but it fails on 2.6.5
        # This problem is fixed in Django 1.1.2 and 1.2
        #
        self.assertEqual(self.client.get('/edit/igor/').status_code, 200,
                "Can't view Profile edit page after login")

    def test_profile_edit(self):
        """ Change some info via web interface """
        self.client.login(username='igor', password='123')

        # Posting wrong data
        post_data = {'contacts':'Test contacts',
                     'biography':'Test biography',
                     'birth_date':'1987-10-32',
                     'first_name':'Igor',
                     'last_name':'Bestuzhev'}
        response = self.client.post('/edit/igor/', post_data)
        self.assertEqual (response.status_code, 200,
                "Posting wrong data didn't return form again")
        self.assertFormError(response, 'prof_form', 'birth_date',
                             'Enter a valid date.')

        # Posting right data
        post_data['birth_date'] = '1987-10-22'
        edit_count_before = LogDB.objects.filter(event_type='DE').count()
        response = self.client.post('/edit/igor/', post_data, follow=True)
        edit_count_after = LogDB.objects.filter(event_type='DE').count()
        self.assertRedirects(response, '/igor/')
        self.assertContains(response, post_data['contacts'])
        self.assertTrue (edit_count_after > edit_count_before,
                "Database change has not been logged")

    def test_settings_context_processor(self):
        """ Tests that every page contains language and timezone\
        from settings.py file
        """
        response = self.client.get('/')
        self.assertContains(response, settings.TIME_ZONE)
        self.assertContains(response, settings.LANGUAGE_CODE)

    def test_template_user_tag(self):
        """ Tests that a page for logined users has a link to user profile"""

        self.client.login(username='igor', password='123')
        response = self.client.get('/')
        self.assertContains(response,
                '<a href="/edit/igor/">Edit profile for Igor Bestuzhev</a>')


