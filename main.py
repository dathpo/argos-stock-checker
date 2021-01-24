from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from helper import args_parser


class ArgosScraper:
    def __init__(self, product_id, postcode):
        self.product_id = product_id
        self.postcode = postcode
        self.options = Options()
        self.driver = None
        self.wait = None

    def setup(self):
        # self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get("https://www.argos.co.uk/product/{}".format(self.product_id))
        self.wait = WebDriverWait(self.driver, 3)
        assert "Argos" in self.driver.title

    def check_stock(self):
        try:
            self.enter_postcode()
            print("Checking for delivery...")
            no_delivery = self.find_element_by_span_text("Not available for delivery to ")
            if not no_delivery:
                print("Item available for delivery")
                # TODO: Push notification
                return True
            print("Checking for collection...")
            not_in_stock = self.find_element_by_span_text("Not in stock at ")
            if not not_in_stock:
                print("Item available for collection")
                # TODO: Push notification
                return True

            self.search_collection_stores()
            return True
        except Exception as e:
            print(e)
            self.driver.close()
            return False

    def enter_postcode(self):
        print("Entering postcode...")
        postcode_input = self.driver.find_element_by_id("search")
        self.wait.until(ec.staleness_of(postcode_input))
        postcode_input = self.wait.until(ec.visibility_of_element_located((By.ID, "search")))
        postcode_input.send_keys(self.postcode)
        postcode_input.submit()

    def find_element_by_span_text(self, text):
        try:
            self.wait.until(
                ec.presence_of_element_located((By.XPATH, "//span[text()='{}']".format(text))))
            return True
        except TimeoutException:
            return False

    def search_collection_stores(self):
        change_store_link = self.wait.until(
            ec.presence_of_element_located((By.LINK_TEXT, "Change store")))
        change_store_link.send_keys(Keys.RETURN)
        store_locator_btn = self.wait.until(
            ec.presence_of_element_located((By.XPATH, "//button[text()='Tell me where']")))
        store_locator_btn.send_keys(Keys.RETURN)


if __name__ == "__main__":
    args = args_parser()
    scraper = ArgosScraper(args.product_id, args.postcode)
    for i in range(int(args.retry_count)):
        print("New search, product ID: {}, postcode: {}, retry count: {}".format(args.product_id, args.postcode,
                                                                                 args.retry_count))
        scraper.setup()
        if scraper.check_stock():
            break
