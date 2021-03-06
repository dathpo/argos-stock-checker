from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec

from post_request import PostRequest


class ArgosStockChecker:
    def __init__(self, scraper, product_id, postcode):
        self.scraper = scraper
        self.product_id = product_id
        self.postcode = postcode

    def check_stock(self):
        try:
            self.enter_postcode()
            if self.check_for_delivery():
                return True
            return self.check_for_collection()
        except Exception as e:
            print(e)
            return self.scraper.quit(False)

    def enter_postcode(self):
        print("Entering postcode...")
        postcode_input = self.scraper.driver.find_element_by_id("search")
        self.scraper.wait.until(ec.staleness_of(postcode_input))
        postcode_input = self.scraper.wait.until(ec.visibility_of_element_located((By.ID, "search")))
        postcode_input.send_keys(self.postcode)
        postcode_input.submit()

    def check_for_delivery(self):
        print("Checking for delivery...")
        no_delivery = self.scraper.find_element_by_tag_text("span", "Not available for delivery to ")
        if not no_delivery:
            print("Item available for delivery at {}".format(self.postcode))
            PostRequest("delivery", self.product_id, self.postcode).send()
            return self.scraper.quit(True)
        print("Item not available for delivery, checking for collection near {}...".format(self.postcode))

    def check_for_collection(self):
        not_in_stock = self.scraper.find_element_by_tag_text("span", "Not in stock at ")
        if not not_in_stock:
            print("Item available for collection near {}".format(self.postcode))
            PostRequest("local_collection", self.product_id, self.postcode).send()
            return self.scraper.quit(True)
        print("Item not available for collection near {}, searching all UK stores for collection...".format(
            self.postcode))
        self.search_collection_stores()
        if not self.scraper.find_element_by_tag_text("p", "Sorry"):
            print("Item available for collection nationwide")
            PostRequest("collection", self.product_id).send()
            return self.scraper.quit(True)
        print("Item not available nationwide")
        return self.scraper.quit(True)

    def search_collection_stores(self):
        change_store_link = self.scraper.wait.until(
            ec.presence_of_element_located((By.LINK_TEXT, "Change store")))
        change_store_link.send_keys(Keys.RETURN)
        store_locator_btn = self.scraper.wait.until(
            ec.presence_of_element_located((By.XPATH, "//button[text()='Tell me where']")))
        store_locator_btn.send_keys(Keys.RETURN)
