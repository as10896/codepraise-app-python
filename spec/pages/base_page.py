from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def exists(self, locator: Tuple[str, str]) -> bool:
        return bool(
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(locator)
            )
        )

    def not_exists(self, locator: Tuple[str, str]) -> bool:
        return bool(
            WebDriverWait(self.driver, 10).until_not(
                EC.presence_of_element_located(locator)
            )
        )

    def is_visible(self, locator: Tuple[str, str]) -> bool:
        return bool(
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(locator)
            )
        )

    def is_not_visible(self, locator: Tuple[str, str]) -> bool:
        return bool(
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(locator)
            )
        )

    def do_click(self, locator: Tuple[str, str]) -> None:
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator)
        ).click()

    def send_keys(self, locator: Tuple[str, str], text: str) -> None:
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(locator)
        ).send_keys(text)

    def get_element_text(self, locator: Tuple[str, str]) -> str:
        element: WebElement = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(locator)
        )
        return element.text
