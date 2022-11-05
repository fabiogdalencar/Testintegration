import pytest
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.CheckoutPage import CheckOutPage
from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass

class TestOne(BaseClass):

    def test_e2e(self):
        log = self.getLogger()
        homePage = HomePage(self.driver)
        checkoutpage = homePage.shopItems()
        log.info("getting all the card titles")
        cards = checkoutpage.getCardTitles()
        i = -1
        for card in cards:
            i = i + 1
            cardText = card.text
            log.info(cardText)
            if cardText == "Blackberry":
                checkoutpage.getCardFooter()[i].click()

        e = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[class*='btn-primary']")))
        e.click()

        confirmpage = checkoutpage.checkOutItems()
        log.info("Entering country name as ind")
        e = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "country")))
        e.send_keys("ind")
        # time.sleep(5)
        self.verifyLinkPresence("India")

        e = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "India")))
        e.click()
        e = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='checkbox checkbox-primary']")))
        e.click()
        e = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[type='submit']")))
        e.click()
        textMatch = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[class*='alert-success']")))
        log.info("Text received from application is "+textMatch.text)

        assert ("Success! Thank you!" in textMatch.text)
