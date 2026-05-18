# shoppingcli/storage.py
"""Загрузка и сохранение данных в JSON."""

import json
import os
from .exceptions import StorageError

DATA_FILE = 'shopping_data.json'

def load_purchases():
    """Загружает список покупок из файла. Если файла нет — возвращает пустой список."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise StorageError(f"Файл {DATA_FILE} должен содержать список, а не {type(data).__name__}")
            return data
    except json.JSONDecodeError as e:
        raise StorageError(f"Ошибка разбора JSON в {DATA_FILE}: {e}")
    except IOError as e:
        raise StorageError(f"Ошибка доступа к файлу {DATA_FILE}: {e}")

def save_purchases(purchases):
    """Сохраняет список покупок в файл."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(purchases, f, indent=4, ensure_ascii=False)
    except IOError as e:
        raise StorageError(f"Не удалось сохранить данные в {DATA_FILE}: {e}")