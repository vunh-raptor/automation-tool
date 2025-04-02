from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import logging
from Common.db_connection import DBConnection as db

class web_element:
    def __init__(self, flag: bool, value: any = None) -> None:
        """This is the init function for web_element object

        Args:
            flag (bool): True if this object hold any WebElement object inside, and vice versa
            value (any): This is intend to contain the WebElement object
        """
        
        self.flag = flag
        if flag:
            self.value = value
        else:
            logging.warning("Creating an empty object")

    def return_element(self) -> WebElement:
        """Returns the contained WebElement

        Returns:
            WebElement: If the flag of the object is true, the WebElement is returned.
        """
        if self.flag:
            return self.value

    def click(self) -> bool:
        """Click the contained Element

        Returns:
            bool: True if the click is sent, and False if there's no element to click.
        """
        if self.flag:
            self.value.click()
            return True
        else:
            logging.critical("There is no element to click.")
            return False

    def send_keys(self, keys: str) -> bool:
        """Send keys to the contained Element.

        Args:
            keys (str): The string of keys that should be sent.

        Returns:
            bool: True if the keys are sent, and False if there's no element to send the keys to.
        """
        if self.flag:
            self.value.send_keys(keys)
            return True
        else:
            logging.critical("There is no element to send keys to.")
            return False
        

    def get_child_element(self) -> int:
        """Return the number of child elements of the element

        Returns:
            int: Number of the child element. Return 0 if there's no element found
        """
    def clearText(self) -> bool:
        self.send_keys(Keys.CONTROL + "a")
        self.send_keys(Keys.DELETE)
        return self.value.text == ''
    
    def get_value(self):
        """get value of web element field

        Returns:
            value of field in text
        """
        return self.value.text    