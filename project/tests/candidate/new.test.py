import unittest
import time
import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

load_dotenv(os.path.join('./project/tests', '.env'))

app_user = os.getenv('APP_USER')
app_psw = os.getenv('APP_PSW')

class Login(unittest.TestCase):

  def setUp(self):
    self.driver = webdriver.Firefox()
    self.driver.get("http://127.0.0.1:8000/login")
    current_url = self.driver.current_url

    elem = self.driver.find_element_by_name("username")
    elem.clear()
    elem.send_keys(app_user)

    elem = self.driver.find_element_by_name("password")
    elem.clear()
    elem.send_keys(app_psw)

    elem.send_keys(Keys.RETURN)

    WebDriverWait(self.driver, 3).until(EC.url_changes(current_url))
  
  # def test_invalid(self):
  #   self.driver.get("http://127.0.0.1:8000/candidato/nuevo")
    
  #   elem = self.driver.find_element_by_name("guardar_empezar_inv")
  #   elem.send_keys(Keys.RETURN)

  #   time.sleep(1)

  #   elem = self.driver.find_element_by_id("msg")
  #   self.assertEqual(elem.text, "- Favor de llenar los campos marcados con *")

  #   errors = self.driver.find_elements_by_class_name("errorlist")
  #   self.assertEqual(len(errors), 5)
  
  def test_valid_save_and_investigation(self):
    self.driver.get("http://127.0.0.1:8000/candidato/nuevo")
    current_url = self.driver.current_url

    new_id = 4 #Persona.objects.all().count() + 1

    elem = self.driver.find_element_by_id("id_candidato-nombre")
    elem.clear()
    elem.send_keys("candidato_" + str(new_id))

    elem = self.driver.find_element_by_id("id_investigacion-puesto")
    elem.clear()
    elem.send_keys("puesto")

    elem = self.driver.find_element_by_id("id_investigacion-compania-nombre")
    elem.click()

    elem = self.driver.find_element_by_css_selector("#selectEmpresaFormaModal #modal-lista-empresas .btn")
    elem.click()

    elem = Select(self.driver.find_element_by_id("id_investigacion-contacto"))
    elem.select_by_index(2)

    elem = Select(self.driver.find_element_by_id("id_investigacion-agente"))
    elem.select_by_index(2)

    elem = self.driver.find_element_by_name("guardar_empezar_inv")
    elem.send_keys(Keys.RETURN)

    WebDriverWait(self.driver, 3).until(EC.url_changes(current_url))

    self.assertIn("candidato/investigacion", self.driver.current_url)
    self.assertIn("editar/exito", self.driver.current_url)
  
  def tearDown(self):
    self.driver.close()

if __name__ == "__main__":
  unittest.main()
