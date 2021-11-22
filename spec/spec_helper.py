import os

os.environ["ENV"] = "test"


from .test_load_all import *

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

HOMEPAGE = "http://localhost:3030"
