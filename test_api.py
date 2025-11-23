import requests
import pytest
import random

BASE_URL = "https://qa-internship.avito.com"
SELLER_ID = random.randint(111111, 999999)
created_item_id = None


def test_1_create_item():
    global created_item_id
    endpoint = f"{BASE_URL}/api/1/item"

    payload = {
        "sellerID": SELLER_ID,
        "name": f"Test Phone {SELLER_ID}",
        "price": 55000,
        "statistics": {
            "contacts": 3,
            "likes": 10,
            "viewCount": 100
        }
    }

    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200, f"Error: {response.text}"

    data = response.json()
    print(f"Created item response: {data}")

    status_message = data.get('status', '')
    if 'Сохранили объявление - ' in status_message:
        created_item_id = status_message.split(' - ')[1]

    assert created_item_id is not None


def test_2_get_item_by_id():
    global created_item_id
    if not created_item_id:
        pytest.skip("Item ID not found")

    endpoint = f"{BASE_URL}/api/1/item/{created_item_id}"
    response = requests.get(endpoint)

    assert response.status_code == 200

    data = response.json()
    if isinstance(data, list):
        item = data[0]
    else:
        item = data

    assert item['sellerId'] == SELLER_ID


def test_3_get_items_by_seller():
    endpoint = f"{BASE_URL}/api/1/{SELLER_ID}/item"

    response = requests.get(endpoint)

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)

    if created_item_id:
        ids_in_response = [item['id'] for item in data]
        assert created_item_id in ids_in_response


def test_4_get_statistics():
    global created_item_id
    if not created_item_id:
        pytest.skip("Item ID not found")

    endpoint = f"{BASE_URL}/api/1/statistic/{created_item_id}"
    response = requests.get(endpoint)

    assert response.status_code == 200
    data = response.json()

    if isinstance(data, list):
        stats = data[0]
    else:
        stats = data

    assert "likes" in stats
    assert "viewCount" in stats
    assert "contacts" in stats
    