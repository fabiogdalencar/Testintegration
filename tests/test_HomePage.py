
from selenium.webdriver.support.select import Select
from selenium import webdriver
import pytest

from TestData.HomePageData import HomePageData
from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


test_HomePage_data = {'firstname': "Rahul", "lastname": "shetty", "gender": "Male"}



class TestHomePage(BaseClass):

    def test_formSubmission(self,getData):
        log = self.getLogger()
        homepage= HomePage(self.driver)
        log.info("first name is "+test_HomePage_data["firstname"])
        '''homepage.getName().send_keys(test_HomePage_data["firstname"])
        homepage.getEmail().send_keys(test_HomePage_data["lastname"])
        homepage.getCheckBox().click()'''
        e = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > app-root > form-comp > div > form > div:nth-child(1) > input")))
        e.send_keys(test_HomePage_data["firstname"])
        e = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, "email")))
        e.send_keys(test_HomePage_data["lastname"])
        e = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "exampleCheck1")))
        e.click()
        self.selectOptionByText(homepage.getGender(), test_HomePage_data["gender"])

        homepage.submitForm().click()

        alertText = homepage.getSuccessMessage().text

        assert ("Success" in alertText)
        self.driver.refresh()

    @pytest.fixture(params=HomePageData.getTestData("Testcase2"))
    def getData(self, request):
        return request.param

