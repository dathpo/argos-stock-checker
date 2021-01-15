from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.argos.co.uk/product/6084934")
assert "Argos" in driver.title

try:
    driver.implicitly_wait(2)
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
    postcode_input = WebDriverWait(driver, 3, ignored_exceptions=ignored_exceptions).until(
        ec.presence_of_element_located((By.ID, "search")))
    postcode_input.send_keys("G4 9EH")
    postcode_input.submit()
    change_store_link = WebDriverWait(driver, 2).until(
        ec.presence_of_element_located((By.LINK_TEXT, "Change store")))
    change_store_link.send_keys(Keys.RETURN)
    store_locator_btn = WebDriverWait(driver, 2).until(
        ec.presence_of_element_located((By.XPATH, '//button[text()="Tell me where"]')))
    store_locator_btn.send_keys(Keys.RETURN)
    # print(driver.page_source.encode("utf-8"))
finally:
    driver.close()
