from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class BookShopPage:
    def __init__(self, seleniumDriver, url):
        self.driver = seleniumDriver
        self.url = url
        self.wait = 20
        self.actions = ActionChains(seleniumDriver)

    def get_book_shop(self):
        self.driver.get(self.url)

    def search_for_the_book(self, criteria):
        search_elem = self.driver.find_element(
            By.CSS_SELECTOR, ".header-search__input")
        search_elem.send_keys(criteria)
        find_elem = self.driver.find_element(
            By.CSS_SELECTOR, ".header-search__button")
        find_elem.click()

    def get_shop_products(self):
        return WebDriverWait(self.driver, self.wait).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".products-list article")))

    def click_on_product(self):
        product = self.get_shop_products()[0]
        self.actions.move_to_element(product).click().perform()

    def add_product_to_chart_click(self):
        button = WebDriverWait(self.driver, self.wait).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-offer-header__buttons")))
        button.click()

    def go_to_cart(self):
        button = WebDriverWait(self.driver, self.wait).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".header-cart.sticky-header__controls-item")))
        button.click()

    def get_cart_products(self):
        return self.driver.find_elements(
            By.CSS_SELECTOR, ".cart-item")
