import unittest
import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv(os.path.join('./project/tests', '.env'))

app_user = os.getenv('APP_USER')
app_psw = os.getenv('APP_PSW')

class Login(unittest.TestCase):

  def setUp(self):
    self.driver = webdriver.Firefox()
  
  def test_login(self):
    self.driver.get("http://127.0.0.1:8000/")
    current_url = self.driver.current_url

    elem = self.driver.find_element_by_name("username")
    elem.clear()
    elem.send_keys(app_user)

    elem = self.driver.find_element_by_name("password")
    elem.clear()
    elem.send_keys(app_psw)

    elem.send_keys(Keys.RETURN)

    WebDriverWait(self.driver, 3).until(EC.url_changes(current_url))

    elem = self.driver.find_element_by_class_name("greeting-msg")
    self.assertEqual(elem.text, "Hola Admint!")

  
  def tearDown(self):
    self.driver.close()

if __name__ == "__main__":
  unittest.main()
