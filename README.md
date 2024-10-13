# Final-Qualification

## Final-Qualification Project

```
Тестирование книжного онлайн-магазина: https://www.chitai-gorod.ru/

```

## Запуск UI тестов
```
pytest .\Tests\test_ui.py

```

## Запуск API тестов
```
pytest .\Tests\test_api.py

```

## UI-тесты: 

### 1. Найти товар в поиске по имени на кириллице : Манюня;
### 2. Найти товар в поиске по его id :3022420;
### 3. Добавление товара в корзину с помощью кнопки "Купить": книга "Пес по имени Мани";
### 4. Увеличение количества товара в корзине с помощью + : книга "Пес по имени Мани" учеличить до 2-х штук;
### 5. Корректное суммирование стоимости товаров в корзине;
### 6. Удаление товара из корзины: книга "Манюня"

## API-тесты: 
Base-URL: https://web-gate.chitai-gorod.ru/api/v1/cart

## Позитивные проверки:
### 1. Добавление товара в корзину: id:2248089
```
Post-запрос
URL: {{Base_url}}/product
Body: {"id":2248089,"adData":{"item_list_name":"product-page"}}
Далее здесь же вторым шагом идет: проверка этого товара в корзине:
GET-запрос
URL: {{Base_url}}
```
### 2. Увеличение количества товара в корзине
```
PUT-запрос
URL: {{Base_url}}
BODY: [{"id":132850748,"quantity":4}]
Далее здесь же вторым шагом идет: проверка этого товара в корзине:
GET-запрос
URL: {{Base_url}}
```
### 3. Удаление товара из корзины
```
Delete-запрос 
URL: {{Base_url}}/product/132850748
Привязываем конкретное id товара
Body нет
Далее здесь же вторым шагом идет: проверка этого товара в корзине:
GET-запрос
URL: {{Base_url}}
```
## Негативные проверки: 

### 4. Изменение количества товара на несуществующее количество
```
Первый шаг: Добавить товар в корзину
Post-Запрос 
URL:{{Base_url}}/product
BODY: {"id":2884565,"adData":{"item_list_name":"product-page"}}

Второй шаг: Изменить количество товара на несуществующее количество товара
PUT-Запрос 
URL: {{Base_url}}
BODY: [{"id":131920052,"quantity":500}]
```
### 5. Добавление несуществующего товара в корзину
```
POST-запрос
URL: {{Base_url}}/product
BODY: {"id":1111111,"adData":{"item_list_name":"product-page"}}
```