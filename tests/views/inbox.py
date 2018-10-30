import unittest
from selenium import webdriver
from apps.users.models import User
from apps.products.models import Category, Product
from apps.inbox.models import Message
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time


class InboxFunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        super(InboxFunctionalTest, self).setUpClass()
        self.browser = webdriver.Firefox()
        user = User.objects.create(email='youruser@test.com')
        user.set_password("yourpassword")
        user.save()
        user = User.objects.create(email='seconduser@test.com')
        user.set_password("yourpassword")
        user.save()
        return ""

    def tearDown(self):
        User.objects.filter(email="youruser@test.com").delete()
        User.objects.filter(email="seconduser@test.com").delete()
        Message.objects.all().delete()
        self.browser.quit()

    def _login_user(self, email="youruser@test.com", password="yourpassword"):
        self.browser.get(self.live_server_url + '/login')
        time.sleep(2)
        email_field = self.browser.find_element_by_id('email')
        password_field = self.browser.find_element_by_id('password')
        email_field.send_keys(email)
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
        time.sleep(2)

    def _create_user(self, email, password):
        user = User.objects.create(email=email)
        user.set_password(password)
        user.save()

    def _create_message(self, second_user):
        url = '/panel/inbox/create/{}'.format(second_user.id)
        self.browser.get(self.live_server_url + url)
        time.sleep(2)
        content = self.browser.find_element_by_id('content')
        send = self.browser.find_element_by_id("send")
        content.send_keys("Testing Creation")
        send.click()
        time.sleep(2)

    def test_send_message_to_user_successful(self):
        self._login_user()
        second_user = User.objects.last()
        self._create_message(second_user)
        try:
            self.browser.find_element_by_id('inbox_title')
            return True
        except NoSuchElementException:
            return False
        return False

    def test_send_message_to_user_fail_for_login(self):
        self._login_user(password="X")
        second_user = User.objects.last()
        url = '/panel/inbox/create/{}'.format(second_user.id)
        self.browser.get(self.live_server_url + url)
        time.sleep(2)
        try:
            self.browser.find_element_by_id('content')
            return False
        except NoSuchElementException:
            return True
        return False

    def test_read_message_from_user_participant_successful(self):
        self._login_user(password="yourpassword")
        time.sleep(2)
        second_user = User.objects.filter(email="youruser@test.com").first()
        self._create_message(second_user)
        url = '/panel/inbox/{}'.format(second_user.id)
        self.browser.get(self.live_server_url + url)
        time.sleep(2)
        try:
            self.browser.find_element_by_id('content')
            return True
        except NoSuchElementException:
            return False
        return False

    def test_read_message_from_user_not_participant_participant_fail(self):
        self._create_user("extra@test.com", "extra")
        time.sleep(2)
        self._login_user(email="extra@test.com", password="extra")
        time.sleep(2)
        extra = User.objects.filter(email="extra@test.com").first()
        second_user = User.objects.filter(email="youruser@test.com").first()
        self._create_message(second_user)
        message = Message.objects.exclude(from_user=extra, to_user=extra).first()
        second_user = User.objects.last()
        url = '/panel/inbox/{}'.format(message.id)
        self.browser.get(self.live_server_url + url)
        time.sleep(2)
        try:
            self.browser.find_element_by_id('content')
            return False
        except NoSuchElementException:
            return True
        return False
