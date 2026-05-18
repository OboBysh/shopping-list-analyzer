# tests/test_logic.py
import pytest
from shoppingcli.logic import add_purchase, get_all_purchases, delete_purchase, filter_by_date, filter_by_category
from shoppingcli.exceptions import ValidationError, PurchaseNotFoundError
from shoppingcli.storage import DATA_FILE
import os

@pytest.fixture
def clean_data():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    yield
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

def test_add_purchase(clean_data):
    pid = add_purchase("Хлеб", "Продукты", "2025-03-10", 50.0)
    assert pid == 1
    purchases = get_all_purchases()
    assert len(purchases) == 1
    assert purchases[0]['name'] == "Хлеб"

def test_add_invalid_name(clean_data):
    with pytest.raises(ValidationError):
        add_purchase("", "Продукты", "2025-03-10", 50)

def test_add_negative_price(clean_data):
    with pytest.raises(ValidationError):
        add_purchase("Молоко", "Продукты", "2025-03-10", -10)

def test_delete(clean_data):
    pid = add_purchase("Масло", "Продукты", "2025-03-10", 100)
    assert delete_purchase(pid) is True
    with pytest.raises(PurchaseNotFoundError):
        delete_purchase(pid)

def test_filter_date(clean_data):
    add_purchase("A", "Cat1", "2025-03-10", 10)
    add_purchase("B", "Cat2", "2025-03-15", 20)
    all_p = get_all_purchases()
    filtered = filter_by_date(all_p, "2025-03-10", "2025-03-10")
    assert len(filtered) == 1
    assert filtered[0]['name'] == "A"

def test_filter_category(clean_data):
    add_purchase("A", "Продукты", "2025-03-10", 10)
    add_purchase("B", "Транспорт", "2025-03-15", 20)
    all_p = get_all_purchases()
    filtered = filter_by_category(all_p, "продукты")
    assert len(filtered) == 1
    assert filtered[0]['name'] == "A"