# tests/test_storage.py
import pytest
import json
import os
from shoppingcli.storage import load_purchases, save_purchases, DATA_FILE
from shoppingcli.exceptions import StorageError

def test_load_empty():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    data = load_purchases()
    assert data == []

def test_save_and_load():
    test_data = [{'id': 1, 'name': 'Тест', 'category': 'Тест', 'date': '2025-01-01', 'price': 100}]
    save_purchases(test_data)
    loaded = load_purchases()
    assert loaded == test_data
    # cleanup
    os.remove(DATA_FILE)