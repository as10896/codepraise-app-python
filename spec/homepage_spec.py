from typing import Iterator

from .spec_helper import *


@pytest.fixture(scope="module")
def driver() -> Iterator[webdriver.Chrome]:
    options = webdriver.ChromeOptions()
    options.headless = True  # Operating in headless mode
    driver_manager = ChromeDriverManager()
    driver_path: str = driver_manager.install()
    service = Service(driver_path)
    _driver = webdriver.Chrome(service=service, options=options)
    yield _driver
    # to prevent invisible headless browser instances from piling up on your machine
    _driver.close()
    _driver.quit()


@pytest.fixture(autouse=True)
def delete_all_repos() -> None:
    ApiGateway().delete_all_repos()


# HAPPY: should see no content
def test_empty_homepage(driver):
    # GIVEN: user is on the home page without any projects
    page = HomePage(driver)

    # THEN: user should see basic headers, no projects and a welcome message
    assert page.get_element_text(page.title_heading) == "CodePraise"
    assert page.is_visible(page.url_input)
    assert page.is_visible(page.add_button)
    assert page.not_exists(page.repos_table)
    assert "Add" in page.get_element_text(page.success_message)
    assert page.not_exists(page.warning_message)


# HAPPY: should add project with valid URL
def test_adding_new_projects(driver):
    # GIVEN: user is on the home page
    page = HomePage(driver)

    # WHEN: user enters a valid URL for a new repo
    page.add_new_repo("https://github.com/soumyaray/YPBT-app")

    # THEN: user should see their new repo listed in a table
    assert "added" in page.get_element_text(page.success_message)
    assert page.is_visible(page.repos_table)
    assert page.listed_repo(page.first_repo) == {
        "owner": "soumyaray",
        "name": "YPBT-app",
        "gh_url": "https://github.com/soumyaray/YPBT-app",
        "num_contributors": 3,
    }


# HAPPY: should be add multiple projects
def test_adding_multiple_projects(driver):
    # GIVEN: on the homepage
    page = HomePage(driver)

    # WHEN: user enters a valid URL for two new repos
    page.add_new_repo("https://github.com/soumyaray/YPBT-app")
    page.add_new_repo("https://github.com/ThxSeafood/thxseafood-app")

    # THEN: user should see both new repos listed in a table
    assert page.exists(page.repos_table)
    assert page.repos_listed_count == 2

    assert page.listed_repo(page.first_repo) == {
        "owner": "soumyaray",
        "name": "YPBT-app",
        "gh_url": "https://github.com/soumyaray/YPBT-app",
        "num_contributors": 3,
    }

    assert page.listed_repo(page.second_repo) == {
        "owner": "ThxSeafood",
        "name": "thxseafood-app",
        "gh_url": "https://github.com/ThxSeafood/thxseafood-app",
        "num_contributors": 2,
    }


# BAD: should not accept incorrect URL
def test_incorrect_github_url(driver):
    # GIVEN: user is on the home page
    page = HomePage(driver)

    # WHEN: user enters an invalid URL
    page.add_new_repo("http://bad_url")

    # THEN: user should see an error alert and no table of repos
    assert "Invalid" in page.get_element_text(page.warning_message)
    assert page.not_exists(page.repos_table)


# SAD: should not accept duplicate repo
def test_duplicate_repo(driver):
    # GIVEN: user is on the home page
    page = HomePage(driver)

    # WHEN: user enters a URL that was previously loaded
    page.add_new_repo("https://github.com/soumyaray/YPBT-app")
    page.add_new_repo("https://github.com/soumyaray/YPBT-app")

    # THEN: user should should see an error message and the existing repo
    assert "already" in page.get_element_text(page.warning_message)
    assert page.repos_listed_count == 1
