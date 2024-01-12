from testCreate import TestCreate
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC

class TestCreatePacote(TestCreate):
  def setup_method(self,endereco, nome,dia,preco):
    self.config()
    self.endereco = endereco
    self.nome = nome
    self.dia = dia
    self.preco = preco #int
  
  def execute_test(self):
    try:
      self.driver.get(self.endereco)
      self.driver.set_window_size(1280, 937)
      self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(4)").click()
      self.driver.find_element(By.ID, "name").click()
      self.driver.find_element(By.ID, "name").send_keys(self.nome)
      self.driver.execute_script(f"document.getElementById('dia').value='{self.dia}'")
      self.driver.find_element(By.ID, "preco").click()
      self.driver.find_element(By.ID, "preco").send_keys(str(self.preco))
      self.driver.find_element(By.CSS_SELECTOR, "button").click()
      WebDriverWait(self.driver, 3).until(EC.alert_is_present())
      self.driver.switch_to.alert.accept()
      self.driver.find_element(By.CSS_SELECTOR, "h1").click()
      return True
    except:
      return False
