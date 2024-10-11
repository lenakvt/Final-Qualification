from selenium import webdriver
from book_shop_page import BookShopPage

driver = webdriver.Chrome()
driver.implicitly_wait(4)

shop_url = 'http://www.chitai-gorod.ru/'
shop_page = BookShopPage(driver, shop_url)
shop_page.get_book_shop()


def test_search_for_the_book_by_name():
    shop_page.search_for_the_book("Манюня")
    products = shop_page.get_shop_products()

    assert len(products) > 1, "Продукт не найден"


def test_search_for_the_book_by_id():
    shop_page.search_for_the_book("3022420")
    products = shop_page.get_shop_products()

    assert len(products) == 1, "Продукт не найден"


def test_add_the_book_to_cart():
    shop_page.search_for_the_book("3022420")
    shop_page.click_on_product()
    shop_page.add_product_to_chart_click()
    shop_page.go_to_cart()

    assert len(shop_page.get_cart_products()) == 1, "В корзине нет продуктов"
