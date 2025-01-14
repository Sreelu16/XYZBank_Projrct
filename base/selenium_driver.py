# @author Sreelakshmi
# Class Description: selenium driver class to be used arcoss all the test cases
from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
from selenium.webdriver.common.alert import Alert
import utilities.custom_logger as cl
import logging
import time
import os
import allure
import utilities.Constants as constant

from base.Reporter import Reporter


class SeleniumDriver():

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screenShot(self, resultMessage):
        """
        Take a screenshot of the current open web page
        """
        fileName = resultMessage + "." + str(round(time.time() *1000)) + ".png"
        if len(fileName) >= 200:
            fileName = str(round(time.time() *1000)) + ".png"
        screenshotDirectory = "../screenshots/"
        relativeFileName = screenshotDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=fileName,
                          attachment_type=allure.attachment_type.PNG)
            self.log.info("Screenshot save to directory: " + destinationFile)
        except:
            self.log.error("### Exception Occurred when taking screenshot")
            print_stack()

    def getTitle(self):
        return self.driver.title

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type" + locatorType + "not correct/supported")
        return False

    def dropdownSelectElement(self, locator, locatorType="id", selector="", selectorType="text",):
        try:
            element = self.getElement(locator, locatorType)
            sel = Select(element)
            if selectorType == "value":
                sel.select_by_value(selector)
                time.sleep(1)
            elif selectorType == "index":
                sel.select_by_index(selector)
                time.sleep(1)
            elif selectorType == "text":
                sel.select_by_visible_text(selector)
                time.sleep(1)
            self.log.info("Element selected with selector: " + str(selector) +
                          " and selectorType: " + selectorType)

        except:
            self.log.error("Element not selected with selector: " + str(selector) +
                       " and selectorType: " + selectorType)
            print_stack()

    def getURL(self):
        '''
        Get the current URL
        :return: current URL
        '''
        currentURL = self.driver.current_url

        return currentURL

    def acceptAlertAndRetunText(self):
        alert=Alert(self.driver)
        value=alert.text
        alert.accept()
        return value

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element found with locator: " + locator +
                          " and locatorType: " + locatorType)
        except:
            self.log.error("Element not found with locator: " + locator +
                          " and locatorType: " + locatorType)
        return element




    def elementClick(self, locator="", locatorType="id", locatorName = 'defaultLocator', element=None):
        """
        Either provide element or a combination of locator and locatorType
        """

        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.click()
            self.log.info("clicked on element with locator: " + locator +
                          " locatorType: " + locatorType)
            time.sleep(3)
        except Exception as e:
            self.log.error("cannot click on the element with locator: " + locator +
                          " locatorType: " + locatorType)

            Reporter.report(self.reports, constant.TYPE_CLICK_ELEMENT, 'Clicking on element: ' + str(locatorName),
                            'Failed to click on element: ' + str(locatorName), constant.TYPE_FAIL)
            print_stack()
            raise e

    def enterInTextBox(self, data, locator="", locatorType="id", element=None):
        """
        enter in TextBox to an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.send_keys(data)
            self.log.info("send data on element with locator: " + locator +
                          " locatorType: " + locatorType)
        except:
            self.log.error("cannot send data on the element with locator: " + locator +
                          " locatorType: " + locatorType)
            print_stack()

    def clearText(self, locator="", locatorType="id", element=None):
        """
        Clear text of an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.clear()
            self.log.info("Clear data of element with locator: " + locator +
                          " locatorType: " + locatorType)
        except:
            self.log.error("cannot clear data of the element with locator: " + locator +
                          " locatorType: " + locatorType)
            print_stack()

    def getText(self, locator="", locatorType="id", element=None, info=""):
        """
        Get 'Text' on an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                self.log.debug("In locator condition")
                element = self.getElement(locator, locatorType)
            self.log.debug("Before finding text")
            text = element.text
            self.log.debug("After finding element, size is: " + str(len(text)))
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) !=0:
                self.log.info("Getting text on element :: " + info)
                self.log.info("The text is :: '" + text + "'")
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def isElementPresent(self, locator="", locatorType="id", element=None):
        """
        Check if element is present
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element found with locator: " + locator +
                              " and locatorType: " + locatorType)
                return True
            else:
                self.log.error("Element not found with locator: " + locator +
                              " and locatorType: " + locatorType)
                return False
        except:
            self.log.error("Element not found with locator: " + locator +
                              " and locatorType: " + locatorType)
            return False


    def waitForElement(self, locator, locatorType = 'id', timeout = 60, pollFrequency = 0.5 ):
        element = None
        try:
            self.log.info("Waiting for maximum :: " + str(timeout) + " :: seconds for element to be clickable")

            wait = WebDriverWait(self.driver, timeout,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            ByType = self.getByType(locatorType)
            element = wait.until(EC.element_to_be_clickable((ByType,locator)))

            self.log.info("Element appeared on the web page")

        except:
            self.log.info("Element not appeared on the web page")
            print_stack()

        return element



    def getAttributeValue(self, locator="", locatorType="id", element=None, attribute=""):
        '''
        get attribute value
        '''
        try:
            if locator:
                self.log.debug("In locator condition")
                element = self.getElement(locator, locatorType)
            attribute_value = element.get_attribute(attribute)
        except:
            self.log.error("Failed to get " + attribute + " in element with locator: " +
                           locator + " and locatorType: " + locatorType)
            print_stack()
            attribute_value = None
        return attribute_value


    def verifyTextMatch(self, message, source, target):

        if source == target:
            Reporter.report(self.reports, constant.TYPE_VALIDATION, message,
                                'Actual Text = ' + str(source) + ' is equal to ' + target)
        else:
            Reporter.report(self.reports, constant.TYPE_VALIDATION, message,
                                'Actual Text = ' + str(source) + ' is not equal to ' + target, constant.TYPE_FAIL)
            assert source == target

    def verifyParticialTextMatch(self, message, source, target):
        if source in target:
            Reporter.report(self.reports, constant.TYPE_VALIDATION, message,
                                'Actual Text = ' + str(source) + ' is equal to ' + target)
        else:
            Reporter.report(self.reports, constant.TYPE_VALIDATION, message,
                                'Actual Text = ' + str(source) + ' is not equal to ' + target, constant.TYPE_FAIL)
            assert source == target

    def VerifyElementisNotPresent(self, locator="", locatorType="id", element=None):
        elementcount=len(self.driver.find_elements(By.XPATH,locator))
        if elementcount==0:
            Reporter.report(self.reports, constant.TYPE_VALIDATION, "Element is deleted",
                            locator+" is not present in UI")
        else:
            Reporter.report(self.reports, constant.TYPE_VALIDATION, "Element is not deleted",
                            locator + " is present in UI",constant.TYPE_FAIL)







