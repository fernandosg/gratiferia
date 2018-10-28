import unittest
from selenium import webdriver
from apps.users.models import User
from apps.products.models import Category, Product
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

class ProductFunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        User.objects.create(email='youruser@test.com', password="yourpassword")
        Category.objects.create(name="Example")


    def tearDown(self):
        self.browser.quit()

    def test_create_product_if_login_successful(self):
         self.browser.get('http://localhost:8000/login')
         email = self.browser.find_element_by_id('email')
         password = self.browser.find_element_by_id('password')
         email.send_keys('youruser@test.com')
         password.send_keys("yourpassword")
         password.send_keys(Keys.ENTER)
         time.sleep(2)
         self.browser.get('http://localhost:8000/products/create')
         name = self.browser.find_element_by_id('id_name')
         description = self.browser.find_element_by_id('id_description')
         contact = self.browser.find_element_by_id("id_contact")
         name.send_keys("Name of product")
         description.send_keys("Description of product")
         contact.send_keys("Contact for request product")
         category = Select(self.browser.find_element_by_id('id_category'))
         category.select_by_value('1')
         name.send_keys(Keys.ENTER)
         time.sleep(2)
         link = self.browser.find_element_by_id('link-to-request').text
         self.assertEqual(link, "Solicitar")
