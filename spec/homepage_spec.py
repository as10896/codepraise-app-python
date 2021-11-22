from .spec_helper import *


@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.headless = True  # Operating in headless mode
    service = Service(ChromeDriverManager().install())
    _driver = webdriver.Chrome(service=service, options=options)
    yield _driver
    # to prevent invisible headless browser instances from piling up on your machine
    _driver.close()
    _driver.quit()


@pytest.fixture(scope="module", autouse=True)
def delete_all_repos():
    ApiGateway().delete_all_repos()


# HAPPY: should see no content
def test_empty_homepage(driver):
    # GIVEN: user is on the home page without any projects
    driver.get(HOMEPAGE)

    # THEN: user should see basic headers, no projects and a welcome message
    assert driver.find_element(By.CSS_SELECTOR, "h1#main_header").text == "CodePraise"
    assert driver.find_element(By.CSS_SELECTOR, "input[name='url']").is_displayed()
    assert driver.find_element(By.CSS_SELECTOR, "input#url_input").is_displayed()
    assert driver.find_element(
        By.CSS_SELECTOR, "button#repo_form_submit"
    ).is_displayed()
    with pytest.raises(NoSuchElementException):
        driver.find_element(By.CSS_SELECTOR, "table#repos_table")

    assert driver.find_element(By.CSS_SELECTOR, "div#flash_bar_success").is_displayed()
    assert "Add" in driver.find_element(By.CSS_SELECTOR, "div#flash_bar_success").text


# HAPPY: should add valid URL
def test_add_new_project(driver):
    # GIVEN: user is on the home page
    driver.get(HOMEPAGE)

    # WHEN: user enters a valid URL for a new repo
    driver.find_element(By.CSS_SELECTOR, "input#url_input").send_keys(
        "https://github.com/soumyaray/YPBT-app"
    )
    driver.find_element(By.CSS_SELECTOR, "button#repo_form_submit").click()
    assert "added" in driver.find_element(By.CSS_SELECTOR, "div#flash_bar_success").text
    with pytest.raises(NoSuchElementException):
        driver.find_element(By.CSS_SELECTOR, "div#flash_bar_danger")

    # THEN: user should see their new repo listed in a table
    assert driver.find_element(By.CSS_SELECTOR, "table#repos_table")
    table = driver.find_element(By.CSS_SELECTOR, "table#repos_table")

    rows = table.find_elements(By.TAG_NAME, "tr")
    assert len(rows) == 2

    row = rows[1]
    assert row.find_element(By.CSS_SELECTOR, "td#td_owner").text == "soumyaray"
    assert row.find_element(By.CSS_SELECTOR, "td#td_repo_name").text == "YPBT-app"
    assert "https" in row.find_element(By.CSS_SELECTOR, "td#td_link").text
    assert (
        len(row.find_element(By.CSS_SELECTOR, "td#td_contributors").text.split(", "))
        == 3
    )
