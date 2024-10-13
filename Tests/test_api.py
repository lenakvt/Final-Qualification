
from configparser import ConfigParser
from services.book_shop_api import BookShopApi
from allure_commons.types import Severity
import allure
import pytest

config = ConfigParser()
config.read("config.ini")

base_url = config.get("api info", "url")
token = config.get("api info", "token")


@pytest.fixture(autouse=True)
def run_around_tests():
    # перед выполнением каждого теста
    global book
    book = BookShopApi(base_url, token)
    book.clear_cart()


@allure.title("Добавление продукта")
@allure.description("Добавить продукт в корзину. Проверить корзину")
@allure.feature("Cart")
@allure.severity(Severity.CRITICAL)
def test_add_product():
    book_id = 2248089

    product = {"id": book_id, "adData": {"item_list_name": "product-page"}}
    with allure.step("Добавить продукт"):
        book.add_product_to_cart(product)

    with allure.step("Получить корзину"):
        cart = book.get_cart()
    
    assert cart['products'][0]['goodsId'] == book_id, "Книга не добавлена"


@allure.title("Увеличение количества")
@allure.description("Добавить продукт в корзину. Увеличить количество")
@allure.feature("Cart")
@allure.severity(Severity.NORMAL)
def test_increase_quantity():
    quantity = 2
    
    with allure.step("Добавить продукт"):
        product = {"id": 2248089, "adData": {"item_list_name": "product-page"}}
        book.add_product_to_cart(product)
        cart = book.get_cart()
        product_id = cart['products'][0]['id']

    with allure.step("Увеличить количество"):
        book.increase_quantity(product_id, quantity)
        cart = book.get_cart()

    assert cart['products'][0]['quantity'] == quantity, """Неверное количество 
    товара"""


@allure.title("Удаление продукта")
@allure.description("Удалить продукт из корзины. Проверить корзину")
@allure.feature("Cart")
@allure.severity(Severity.CRITICAL)
def test_delete_product():
    with allure.step("Добавить продукт"):
        product = {"id": 2248089, "adData": {"item_list_name": "product-page"}}
        book.add_product_to_cart(product)
        cart = book.get_cart()
        product_id = cart['products'][0]['id']
    
    with allure.step("Удалить продукт"):
        is_delete = book.delete_product(product_id)
        cart = book.get_cart()

    assert is_delete, "Продукт не удален"
    assert len(cart['products']) == 0, "В корзине остались товары"


@allure.title("Негативный. Увеличить количество")
@allure.description("Увеличить количество на несуществующую величину")
@allure.feature("Cart")
@allure.severity(Severity.NORMAL)
def test_add_incorrect_quantity():
    with allure.step("Добавить продукт"):
        quantity = 500
        product = {"id": 2248089, "adData": {"item_list_name": "product-page"}}
        book.add_product_to_cart(product)
        cart = book.get_cart()
        product_id = cart['products'][0]['id']

    with allure.step("Увеличить количество"):
        status_code = book.increase_quantity(product_id, quantity)

    assert status_code == 422, "Количество товара"


@allure.title("Негативный. Добавить несуществующий продукт")
@allure.description("Добавить продкут. Проверить корзину.")
@allure.feature("Cart")
@allure.severity(Severity.NORMAL)
def test_add_incorrect_producty():
    with allure.step("Получить корзину"):
        cart = book.get_cart()
        products_length1 = len(cart['products'])

    with allure.step("Добавить продукт"):
        product = {"id": -1, "adData": {"item_list_name": "product-page"}}
        products_length2 = len(cart['products'])
        status_code = book.add_product_to_cart(product)
        
    with allure.step("Получить корзину"):
        cart = book.get_cart()

    assert products_length1 == products_length2
    assert status_code == 422, "Продукт существует"
