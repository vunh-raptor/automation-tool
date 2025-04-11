import logging
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Common.web_element import web_element

class page_object:
    def __init__(
        self,
        path: str = "chromedriver.exe",
    ):
        """This is the init function for the base page_object. Please be reminded that we only use ChromeDriver.

        Args:
            path (str, optional): Path to the ChromeDriver execution file. Defaults to "chromedriver.exe".
        """

        self.default_delay = 0.2
        self.default_timeout = 10

        self.path = path

        self.profile = webdriver.ChromeService(executable_path=self.path)
        self.driver = webdriver.Chrome(service=self.profile)      
        self.wait = WebDriverWait(self.driver, self.default_timeout)

    def headless(self) -> None:
        """This is to generate headless session for chromedriver"""
        service = webdriver.ChromeService(executable_path=self.path)
        op = webdriver.ChromeOptions()
        op.add_argument("--headless")
        op.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(service=service, options=op)

    def search_by_xpath(
        self, xpath: str, timeout: int = 5, delay: float = 0.2
    ) -> web_element:
        """Search an object by XPATH, return a web_element object.

        Args:
            xpath (str): The XPATH to the desired element.
            timeout (int, optional): How much time should the script retry before concluding that there exists no such object. Defaults to 5.
            delay (float, optional): How long should the script wait between each check, measured in second. Defaults to 0.2.

        Returns:
            web_element: The wrapped web_element object contains web_element.flag and web_element.value.
        """
        for count in range(timeout):
            found = False
            try:
                result = self.driver.find_element(By.XPATH, xpath)
                found = True
                break
            except Exception:
                warning = (
                    "Cannot find element "
                    + str(xpath)
                    + ", retry "
                    + str(count)
                    + " time."
                )
                logging.warning(warning)
                sleep(delay)
                continue

        if not found:
            return web_element(flag=found)
        else:
            return web_element(found, result)
        
    def wait_element_to_visible(self, xpath: str) -> bool:
        """this function is wait for the element to be visible in the web page

        Args:
            xpath (str): direct xpath point to specific element

        Returns:
            bool: return true if the element is visible
        """
        # Wait until the element is visible
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return element.is_displayed()

    def click_by_xpath(self, xpath: str, timeout: int = 5, delay: float = 0.2) -> bool:
        """Search an object by XPATH, and click it.

        Args:
            xpath (str): the XPATH to the desired element
            timeout (int, optional): How much time should the script retry before concluding that there exists no such object. Defaults to 5.
            delay (float, optional): How long should the script wait between each check, measured in second. Defaults to 0.2.

        Returns:
            bool: True if the element is clicked, and False if there's no such element found.
        """
        element = self.search_by_xpath(xpath=xpath, timeout=timeout, delay=delay)
        return element.click()

    def send_keys_by_xpath(
        self, xpath: str, keys: str, timeout: int = 5, delay: float = 0.2
    ) -> bool:
        """Search an object by XPATH, and send the desired keys to it.

        Args:
            xpath (str): The XPATH to the desired element.
            keys (str): The string of keys that should be sent.
            timeout (int, optional): How much time should the script retry before concluding that there exists no such object. Defaults to 5.
            delay (float, optional): How long should the script wait between each check, measured in second. Defaults to 0.2.

        Returns:
            bool: True if the keys are sent, and False if there's no such element found.
        """
        element = self.search_by_xpath(xpath=xpath, timeout=timeout, delay=delay)
        return element.send_keys(keys=keys)

    def get(self, url: str):
        """Go to a specific URL

        Args:
            url (str): the desired URL.
        """
        self.driver.get(url=url)
            
    def select_dropdown_value(
        self, xpath: str, value: str, timeout: int = 5, delay: float = 0.2
    ) -> None:
        """Select a desired element by value

        Args:
            xpath (str): XPATH for dropdown box
            value (str): value to select - by value that set in the back-end of the website
            timeout (int, optional): _description_. Defaults to 5.
            delay (float, optional): _description_. Defaults to 0.2.
        """
        for count in range(timeout):
            try:
                select = Select(self.driver.find_element(By.XPATH, xpath))
                select.select_by_value(value=value)
                break
            except Exception as e:
                warning = (
                    "Cannot find drop down box "
                    + str(xpath)
                    + ", retry "
                    + str(count)
                    + " time."
                    + ", " + str(e)
                )
                logging.warning(warning)
                sleep(delay)
                continue
            
    def select_dropdown_by_visible_text(
        self, xpath: str, value: str, timeout: int = 5, delay: float = 0.2
    ) -> None:
        """Select a desired element by visible text

        Args:
            xpath (str): XPATH for dropdown box
            value (str): value to select - by visible text shown on GUI
            timeout (int, optional): _description_. Defaults to 5.
            delay (float, optional): _description_. Defaults to 0.2.
        """
        for count in range(timeout):
            try:
                select = Select(self.driver.find_element(By.XPATH, xpath))
                select.select_by_visible_text(text=value)
                break
            except Exception as e:
                warning = (
                    "Cannot find drop down box "
                    + str(xpath)
                    + ", retry "
                    + str(count)
                    + " time."
                    + ", " + str(e)
                )
                logging.warning(warning)
                sleep(delay)
                continue
            
    def select_dropdown_by_contains_text(
        self, xpath: str, value: str, timeout: int = 5, delay: float = 0.2
    ) -> None:
        """Another type of select dropdown, for a variable that contains needed value

        Args:
            xpath (str): XPATH for dropdown box
            value (str): value to select, in this function the value is only a partial string of the correct value
            timeout (int, optional): Defaults to 5.
            delay (float, optional): Defaults to 0.2.
        """
        xpath = xpath + "/option[contains(text(), '" + value + "')]"
        print(xpath)
        for count in range(timeout):
            try:
                self.driver.find_element(By.XPATH, xpath).click()
                break
            except Exception as e:
                warning = (
                    "Cannot find value "
                    + str(xpath)
                    + ", retry "
                    + str(count)
                    + " time."
                    + ", " + str(e)
                )
                logging.warning(warning)
                sleep(delay)
                continue
    
    def accept_the_alert_pop_up(self) -> None:
        """ 
        this function is to accept the alert pop up on the webpage
        """

        WebDriverWait(self.driver, self.default_timeout).until(EC.alert_is_present())
        alert = Alert(self.driver)
        alert.accept()
        
