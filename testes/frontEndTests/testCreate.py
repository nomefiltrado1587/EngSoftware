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

class TestCreate:

    def config(self):
        self.driver = webdriver.Chrome()
        self.vars = {}
    
    def teardown_method(self, method): # FIXME - Método ficou sem ser usado
        self.driver.quit()

    def execute_test(self):
        pass