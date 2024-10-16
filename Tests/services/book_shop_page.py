from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import re
import allure


class BookShopPage:
    def __init__(self, seleniumDriver, url: str):
        self.driver = seleniumDriver
        self.url = url
        self.wait = 20
        self.actions = ActionChains(seleniumDriver)

    @allure.step("получить сайт")
    def get_book_shop(self):
        self.driver.get(self.url)

    @allure.step("поиск продукта")
    def search_for_the_book(self, criteria: str):
        search_elem = self.driver.find_element(
            By.CSS_SELECTOR, ".header-search__input")
        search_elem.clear()
        search_elem.send_keys(criteria)
        find_elem = self.driver.find_element(
            By.CSS_SELECTOR, ".header-search__button")
        find_elem.click()

    @allure.step("получить все продукты")
    def get_shop_products(self) -> object:
        selector = ".products-list article"
        return WebDriverWait(self.driver, self.wait).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))

    @allure.step("кликнуть на продкут")
    def click_on_product(self):
        product = self.get_shop_products()[0]
        self.actions.move_to_element(product).click().perform()

    @allure.step("кликнуть на кнопку добавления продукта")
    def add_product_to_chart_click(self):
        selector = ".product-offer-header__buttons"
        button = WebDriverWait(self.driver, self.wait).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        button.click()

    @allure.step("кликнуть на кнопке перехода в корзину")
    def go_to_cart(self):
        selector = ".header-cart.sticky-header__controls-item"
        button = WebDriverWait(self.driver, self.wait).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        button.click()

    @allure.step("получить все продукты из корзины")
    def get_cart_products(self) -> list:
        selector = ".cart-item"
        WebDriverWait(self.driver, self.wait).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        return self.driver.find_elements(
            By.CSS_SELECTOR, ".cart-item")

    @allure.step("увеличить количество на 1")
    def increase_quantity_by_one(self):
        selector = ".product-quantity__button.product-quantity__button--right"
        button = WebDriverWait(self.driver, self.wait).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        button.click()

    @allure.step("получить текущее количесвто продукта")
    def get_quantity(self) -> str:
        selector = ".product-quantity__counter"
        input = WebDriverWait(self.driver, self.wait).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        return input.get_attribute('value')

    @allure.step("рассчитать цену всех товаров в списке в корзине")
    def get_all_products_price(self) -> int:
        selector = ".product-price__value.product-price__value--discount"
        WebDriverWait(self.driver, self.wait).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

        elements = self.driver.find_elements(
            By.CSS_SELECTOR, selector)

        total = 0
        for el in elements:
            total += self.__get_price(el.text)

        return total

    @allure.step("получить цену Итого в корзине")
    def check_total(self) -> int:
        selector = ".info-item.cart-sidebar__item-summary .info-item__value"
        WebDriverWait(self.driver, self.wait).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

        element = self.driver.find_element(
            By.CSS_SELECTOR, selector)

        total = self.__get_price(element.text)
        return total

    def __get_price(self, price_with_curr: str) -> int:
        trim = re.compile(r'[^\d.,]+')
        return int(trim.sub('', price_with_curr))
