import time  # For debugging

from django.core.urlresolvers import resolve
from django.test import TestCase  # Augmented version of std unittest.TestCase
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.db import models

from timesheets.models import Program  # To test Models
from timesheets.forms import ProgramForm  # To test Forms
from timesheets.views import blank

""" Unit Tests help you write code that is clean and bug free
    Each line of production code we write should be tested by at least
    one of our unit tests

    Run specific tests for an application using: python manage.py test

    COVERAGE
    Check test coverage with: coverage run manage.py test
    Run test coverage report with: coverage html --include="timesheets/*.*" and
    then look under folder 'htmlcov' > 'index.html'
"""

### Test to see if Pages are routed correctly

# Blank Page - url(r'^$'')

'''
class SmokeTest(TestCase):
    """ A test that will deliberately fail so we can see error output"""
    def test_bad_maths(self):
        self.assertEqual(1 + 1, 3)
'''


class MainPageTest(TestCase):

    def test_root_url_resolves_to_blank_view(self):
        found = resolve('/')  # resolves this url to map with function in views
        self.assertEqual(found.func, blank)  # Found the url and function

    def test_blank_page_returns_correct_html(self):
        request = HttpRequest()  # What Django sees when browser asks for page
        response = blank(request)  # Pass it to our view named 'blank' and get this response

        # Check response's start and end contents manually (don't do, too tedious)
        # response.content is raw bytes, not a Python string so needs b'' syntax
        #self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
        #self.assertIn(b'<h1>Welcome</h1>', response.content)
        #self.assertIn(b'</html>', response.content)
        #print repr(response.content)

        # Get template's html for blank, check that it's the correct response for blank view
        expected_html = render_to_string("blank.html")
        self.assertEqual(response.content.decode(), expected_html)
        # Decode helps us convert reponse's content bytes to unicode strings
        #print repr(response.content.decode()) # Print response for debugging
        #time.sleep(10)

#class ProgramListViewTest(TestCase):

    #def test_display_all_items(self):

        #Program.objects.create()

        #response = self.client.get('')  # Use Django's test client

        #self.assertContains(response, '')


#class TimesheetPageTest(TestCase):

    #def test_timesheet_list_view_resolves(self):
    #    found = resolve('timesheet')
    #    self.assertEqual(found.func, ProgramListView)


'''

class ProgramModelTests(TestCase):
    """ Program Model Tests """

    def test_str(self):
        notes = Program(
                          notes='Hello world!')

        self.assertEquals(str(notes),
                          'Hello world',
                          )

'''


### Form Tests Below

class ProgramFormTest(TestCase):
    """ Program Form Test """
    def test_validation(self):
        form_data = {
            'hours_spent': 7,
            'minutes_spent': 10,
            'notes': 'X' * 300
        }
        form = ProgramForm(data=form_data)
        self.assertFalse(form.is_valid())



### Main
if __name__ == '__main__':
    unittest.main(warnings='ignore')
