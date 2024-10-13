import requests
import allure


class BookShopApi:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @allure.step("очистить корзину")
    def clear_cart(self) -> str | bool:
        url = f"{self.base_url}/cart"
        resp = requests.delete(url)
        if (resp.status_code != 200):
            return resp.status_code

        return resp.status_code == 200

    @allure.step("получить продукты")
    def get_procucts(self, search_params) -> object:
        url = f"{self.base_url}/search/product"
        resp = requests.get(url, params=search_params, headers=self.headers)
        return resp.json()

    @allure.step("получить корзину")
    def get_cart(self) -> object:
        url = f"{self.base_url}/cart"
        resp = requests.get(url, headers=self.headers)
        return resp.json()

    @allure.step("добавить продукт в корзину")
    def add_product_to_cart(self, payload: dict) -> str | bool:
        url = f"{self.base_url}/cart/product"
        resp = requests.post(url, json=payload, headers=self.headers)

        if (resp.status_code != 200):
            return resp.status_code

        return resp.status_code == 200

    @allure.step("увеличить количество")
    def increase_quantity(self, product_id: int, quantity: int) -> str | bool:
        url = f"{self.base_url}/cart"
        payload = [{"id": product_id, "quantity": quantity}]
        resp = requests.put(
            url, json=payload,
            headers=self.headers)

        if (resp.status_code != 204):
            return resp.status_code

        return resp.status_code == 204

    @allure.step("удалить продукт")
    def delete_product(self, product_id: int) -> str | bool:
        url = f"{self.base_url}/cart/product/{str(product_id)}"
        resp = requests.delete(url, headers=self.headers)
        
        if (resp.status_code != 204):
            return resp.status_code

        return resp.status_code == 204
