import unittest

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # Allows us to enter 'keys'

""" Functional Test == Acceptance Test == End-to-End Test  == Black box Test
    Overview: helps you build an application with the right functionality
    and guarantees that you never accidentally break it.  This kind of test
    looks at how the whole application functions (from the outside) and should
    have human readable code (as in telling a story)

    How to run functional tests: python manage.py test functional_tests
    How to run functional and unit tests: python manage.py test
    How to run unit tests for timesheet app only: python manage.py test timesheet

    What this does:
    1.) Starts a Selenium webdriver to pop up a real Firefox browser window
    2.) Use it to open up a web page that we're expecting to be served from the local PC
    3.) Check (making a test assertion) that conditions are met
"""


### Setup
class NewVisitorTest(LiveServerTestCase):
    """ Does landing page load? """

    def setUp(self):
        """ setUp runs before each test, like a try in try/except """
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)  # Implicitly Wait for page to load

    def tearDown(self):
        """ tearDown runs after each test, even if there's an error during the test itself """
        self.browser.quit()

    def test_see_main_page_elements(self):
        """ Can see the main page elements like buttons, links """
        # Will needs to enter in some data; he opens up his browser
        #self.browser.get('http://localhost:8000')  # Local Dev Env (Hard Coded)
        #self.browser.get('http://10.1.1.7')  # Ubuntu Server
        self.browser.get(self.live_server_url)  # uses Django's server

        # Will notices the page title
        self.assertIn('L2H Data', self.browser.title)
        #assert 'L2H Data' in self.browser.title , "The Browser Title is " + self.browser.title

        # Will notices the 'Home' text
        home_nav_bar = self.browser.find_element_by_id('home')
        #print type(sign_in_button)  #<class selenium.webdriver.remote.webelement.WebElement
        #print sign_in_button.text
        self.assertEqual(home_nav_bar.text, 'Home')

        # Will notices the 'Sign In' button
        sign_in_button = self.browser.find_element_by_id('login')
        #print type(sign_in_button)  #<class selenium.webdriver.remote.webelement.WebElement
        #print sign_in_button.text
        self.assertEqual(sign_in_button.text, 'Sign In')

        # Will notices the 'Register' button
        register_button = self.browser.find_element_by_id('register')
        #print type(sign_in_button)  #<class selenium.webdriver.remote.webelement.WebElement
        #print sign_in_button.text
        self.assertEqual(register_button.text, 'Register')

    """
    def test_click_main_page_links(self):
        ''' Can click through to the main page's links '''
        # Click through all the buttons
        home_nav_bar = self.browser.find_element_by_id('home')
        self.browser.click(home_nav_bar)
    """

        # Will enters the registration information and sends an activation email

        # Will confirms the activation email

        # Will clicks on the 'Sign In' tab

        # Will forgets his password 'Forgot'

        # Will has an account and now signs in

'''
class TimesheetTest(unittest.TestCase):
    """ Does Timesheet work? """

    def setUp(self):
        """ setUp runs before each test, like a try in try/except """
        self.browser = webdriver.Firefox()
        #self.browser.implicitly_wait(3)  # Implicitly Wait for page to load

    def tearDown(self):
        """ tearDown runs after each test, even if there's an error during the test itself """
        self.browser.quit()

    def test_see_timesheet_page_elements(self):
        """ Can see the main page elements like buttons, links """
        # Will needs to enter in timesheets; he opens up his browser
        self.browser.get('http://localhost:8000/timesheet')  # Local Dev Environment
        #self.browser.get('http://10.1.1.7')  # Ubuntu Server
'''




"""
class UserLoginAccessSite(unittest.TestCase):
    ''' Can user log in and add, edit, delete times? '''

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)  # Wait for page to load

    def tearDown(self):
        self.browser.quit()

    def test_login_with_dummy_account(self):
        #self.browser.get('http://localhost:8000')  # Get Local Dev Env

        # User clicks on 'Sign In' button and logs in
        self.browser.find_element_by_id('login').click()
        self.browser.find_element_by_id('id_username').send_keys('test')
        self.browser.find_element_by_id('id_password').send_keys('stupid12')
        self.browser.find_elements_by_name('login').send_keys('Keys.ENTER')
        self.browser.implicitly_wait(3)  # Implicitly Wait for page to load


    def test_navigate_to_timesheet(self):
        # User navigates to Timesheet
        self.browser.find_element_by_id('timesheet').click()
        # User clicks to add Time
        self.browser.find_element_by_id('id_program_create').click()
        # Add in Date
        self.browser.find_element_by_id('id_date_select').send_keys('06/01/2014')
"""

# How a Python script checks if it's been executed from the command
# line rather than being imported by another script
if __name__ == '__main__':

    #unittest.main(warnings='ignore')
    unittest.main()
