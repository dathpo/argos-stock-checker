from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class ArgosScraper:
    def __init__(self, product_id):
        self.product_id = product_id
        self.options = Options()
        self.driver = None
        self.wait = None

    def setup(self):
        self.options.add_argument("--headless")               # Add options here
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.get("https://www.argos.co.uk/product/{}".format(self.product_id))
        self.wait = WebDriverWait(self.driver, 5)
        assert "Argos" in self.driver.title

    def find_element_by_tag_text(self, tag, text):
        try:
            self.wait.until(
                ec.presence_of_element_located((By.XPATH, "//{}[text()='{}']".format(tag, text))))
            return True
        except TimeoutException:
            return False

    def quit(self, success):
        self.driver.close()
        return success


if __name__ == "__main__":
    from module_helper import args_parser, main
    args = args_parser()
    main(args)
