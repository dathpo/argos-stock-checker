from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from argos_stock_checker import ArgosStockChecker
from module_helper import args_parser


class ArgosScraper:
    def __init__(self, product_id):
        self.product_id = product_id
        self.options = Options()
        self.driver = None
        self.wait = None

    def setup(self):
        # self.options.add_argument("--headless")               # Add options here
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get("https://www.argos.co.uk/product/{}".format(self.product_id))
        self.wait = WebDriverWait(self.driver, 3)
        assert "Argos" in self.driver.title

    def find_element_by_span_text(self, text):
        try:
            self.wait.until(
                ec.presence_of_element_located((By.XPATH, "//span[text()='{}']".format(text))))
            return True
        except TimeoutException:
            return False

    def quit(self, success):
        self.driver.close()
        return success


if __name__ == "__main__":
    args = args_parser()
    scraper = ArgosScraper(args.product_id)
    stock_checker = ArgosStockChecker(scraper, args.postcode)
    for i in range(int(args.retry_count)):
        print("New search, product ID: {}, postcode: {}, retry count: {}".format(args.product_id, args.postcode,
                                                                                 args.retry_count))
        scraper.setup()
        if stock_checker.check_stock():
            break
