from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from config import get_settings
from typing_helpers import ListedRepo

from .base_page import BasePage


class HomePage(BasePage):

    homepage = get_settings().APP_URL

    warning_message = (By.CSS_SELECTOR, "div#flash_bar_danger")
    success_message = (By.CSS_SELECTOR, "div#flash_bar_success")

    title_heading = (By.CSS_SELECTOR, "h1#main_header")
    url_input = (By.CSS_SELECTOR, "input#url_input")
    add_button = (By.CSS_SELECTOR, "button#repo_form_submit")
    repos_table = (By.CSS_SELECTOR, "table#repos_table")
    rows = (By.CSS_SELECTOR, "table#repos_table > tbody > tr")

    repo_owner = (By.CSS_SELECTOR, "span[id^='repo['][id$='].owner'")
    repo_name = (By.CSS_SELECTOR, "a[id^='repo['][id$='].link'")
    repo_gh_url = (By.CSS_SELECTOR, "a[id^='repo['][id$='].gh_url'")
    repo_num_contributors = (By.CSS_SELECTOR, "span[id^='repo['][id$='].contributors'")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.driver.get(self.homepage)

    @property
    def repos(self) -> List[WebElement]:
        return self.driver.find_elements(*self.rows)

    @property
    def first_repo(self) -> WebElement:
        return self.repos[0]

    @property
    def second_repo(self) -> WebElement:
        return self.repos[1]

    @property
    def repos_listed_count(self) -> int:
        return len(self.repos)

    def add_new_repo(self, github_url: str) -> None:
        self.send_keys(self.url_input, github_url)
        self.do_click(self.add_button)

    def listed_repo(self, repo: WebElement) -> ListedRepo:
        return {
            "owner": repo.find_element(*self.repo_owner).text,
            "name": repo.find_element(*self.repo_name).text,
            "gh_url": repo.find_element(*self.repo_gh_url).text,
            "num_contributors": len(
                repo.find_element(*self.repo_num_contributors).text.split(",")
            ),
        }
