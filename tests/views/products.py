import unittest
from selenium import webdriver
from apps.users.models import User
from apps.products.models import Category, Product
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time

class ProductFunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        super(ProductFunctionalTest, self).setUpClass()
        self.browser = webdriver.Firefox()
        category = Category.objects.create(name="Example")
        user = User.objects.create(email='youruser@test.com')
        user.set_password("yourpassword")
        user.save()
        Product.objects.create(name="Testing", description="X", contact="X", author=user, category=category)

    def tearDown(self):
        User.objects.filter(email="youruser@test.com").delete()
        Category.objects.filter(name="Example").delete()
        Product.objects.filter(name="Testing").delete()
        self.browser.quit()

    def test_create_product_if_login_successful(self):
         self.browser.get(self.live_server_url + '/login')
         email = self.browser.find_element_by_id('email')
         password = self.browser.find_element_by_id('password')
         email.send_keys('youruser@test.com')
         password.send_keys("yourpassword")
         password.send_keys(Keys.ENTER)
         time.sleep(2)
         self.browser.get(self.live_server_url + '/products/create')
         name = self.browser.find_element_by_id('id_name')
         description = self.browser.find_element_by_id('id_description')
         contact = self.browser.find_element_by_id("id_contact")
         name.send_keys("Testing Creation")
         description.send_keys("Description of product")
         contact.send_keys("Contact for request product")
         category = Select(self.browser.find_element_by_id('id_category'))
         category.select_by_value('1')
         name.send_keys(Keys.ENTER)
         time.sleep(2)
         link = self.browser.find_element_by_id('link-to-request').text
         self.assertEqual(link, "Solicitar")

    def test_request_product_if_login_successful(self):
         self.browser.get(self.live_server_url + '/login')
         email = self.browser.find_element_by_id('email')
         password = self.browser.find_element_by_id('password')
         email.send_keys('youruser@test.com')
         password.send_keys("yourpassword")
         password.send_keys(Keys.ENTER)
         time.sleep(2)
         url =  self.live_server_url + ("/products/{}".format(Product.objects.first().slug))
         self.browser.get(url)
         request_link = self.browser.find_element_by_id('link-to-request')
         request_link.click()
         time.sleep(2)
         link = self.browser.find_element_by_id('link-to-request').text
         self.assertEqual(link, "Solicitar")


    def test_request_product_not_allowed_if_not_login(self):
         self.browser.get(self.live_server_url + '/logout')
         time.sleep(1)
         url = self.live_server_url + ("/products/{}".format(Product.objects.first().slug))
         self.browser.get(url)
         try:
             self.browser.find_element_by_id('link-to-request')
         except NoSuchElementException:
             return True
