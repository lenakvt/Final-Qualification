from selenium import webdriver
from configparser import ConfigParser
from services.book_shop_page import BookShopPage
from allure_commons.types import Severity
import pytest
import allure

config = ConfigParser()
config.read("config.ini")
shop_url = config.get("ui info", "url")


@pytest.fixture(autouse=True)
def run_around_tests():
    # перед выполнением каждого теста
    global driver
    global shop
    driver = webdriver.Chrome()
    shop = BookShopPage(driver, shop_url)
    shop.get_book_shop()

    yield
    # после выполнения каждого теста
    driver.quit()


@allure.title("Поиск книги по наименованию")
@allure.description("Поиск книги по названию")
@allure.feature("Shop")
@allure.severity(Severity.NORMAL)
def test_search_for_the_book_by_name():
    with allure.step("поиск книги"):
        shop.search_for_the_book("Манюня")
    with allure.step("запрос списка продуктов"):
        products = shop.get_shop_products()

    assert len(products) > 1, "Продукт не найден"


@allure.title("Поиск книги по идентификатору")
@allure.description("Поиск книги по книжному идентификатору")
@allure.feature("Shop")
@allure.severity(Severity.NORMAL)
def test_search_for_the_book_by_id():
    with allure.step("поиск книги"):
        shop.search_for_the_book("3022420")

    with allure.step("запрос списка продуктов"):
        products = shop.get_shop_products()

    assert len(products) == 1, "Продукт не найден"


@allure.title("Добавление книги в корзину")
@allure.description("Добавление книги. Проверка корзины.")
@allure.feature("Shop")
@allure.severity(Severity.NORMAL)
def test_add_the_book_to_cart():
    with allure.step("добавление книги"):
        shop.search_for_the_book("3022420")
        shop.click_on_product()
        shop.add_product_to_chart_click()

    with allure.step("чтение корзины"):
        shop.go_to_cart()

    assert len(shop.get_cart_products()) == 1, "В корзине нет продуктов"


@allure.title("Добавление двух книг в корзину")
@allure.description("Добавление книг. Проверка корзины.")
@allure.feature("Shop")
@allure.severity(Severity.NORMAL)
def test_add_two_books_to_cart():
    with allure.step("добавление книги 1"):
        shop.search_for_the_book("3022420")
        shop.click_on_product()
        shop.add_product_to_chart_click()

    with allure.step("добавление книги 2"):
        shop.search_for_the_book("2248089")
        shop.click_on_product()
        shop.add_product_to_chart_click()

    with allure.step("чтение корзины"):
        shop.go_to_cart()

    assert len(shop.get_cart_products()) == 2, "В корзине нет продуктов"


@allure.title("Увеличение количества")
@allure.description("Увеличение количества экземляров книги")
@allure.feature("Shop")
@allure.severity(Severity.NORMAL)
def test_add_book_and_increase_quantity():
    with allure.step("поиск и добавление книги"):
        shop.search_for_the_book("3022420")
        shop.click_on_product()
        shop.add_product_to_chart_click()

    with allure.step("чтение корзины"):
        shop.go_to_cart()

    with allure.step("увеличение количества"):
        shop.increase_quantity_by_one()

    assert shop.get_quantity() == "2"


@allure.title("Проверка Итоговой цены товара в корзине")
@allure.description("Проверка Итоговой цены товара в корзине")
@allure.feature("Shop")
@allure.severity(Severity.NORMAL)
def test_check_cart_total():
    with allure.step("поиск и добавление книги 1"):
        shop.search_for_the_book("3022420")
        shop.click_on_product()
        shop.add_product_to_chart_click()

    with allure.step("поиск и добавление книги 2"):
        shop.search_for_the_book("2248089")
        shop.click_on_product()
        shop.add_product_to_chart_click()

    with allure.step("чтение корзины"):
        shop.go_to_cart()

    with allure.step("получение цены всех продуктов"):
        total_products_price = shop.get_all_products_price()

    assert shop.check_total() == total_products_price, """Цена товаров 
    рассчитана не правильно"""
