# shoppingcli/logic.py
"""Бизнес-логика приложения."""

from datetime import datetime
from .storage import load_purchases, save_purchases
from .exceptions import ValidationError, PurchaseNotFoundError

def add_purchase(name: str, category: str, date_str: str, price: float) -> int:
    """
    Добавляет новую покупку.
    :param name: название товара
    :param category: категория (например, 'Продукты', 'Транспорт')
    :param date_str: дата в формате ГГГГ-ММ-ДД
    :param price: стоимость (положительное число)
    :return: ID новой покупки
    :raises ValidationError: при некорректных данных
    """
    # Валидация
    if not name or not name.strip():
        raise ValidationError("Название товара не может быть пустым.")
    if not category or not category.strip():
        raise ValidationError("Категория не может быть пустой.")
    if price <= 0:
        raise ValidationError("Цена должна быть положительным числом.")
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValidationError("Дата должна быть в формате ГГГГ-ММ-ДД (например, 2025-03-10).")

    purchases = load_purchases()
    new_id = max([p['id'] for p in purchases], default=0) + 1
    purchase = {
        'id': new_id,
        'name': name.strip(),
        'category': category.strip(),
        'date': date_str,
        'price': price
    }
    purchases.append(purchase)
    save_purchases(purchases)
    return new_id

def get_all_purchases():
    """Возвращает список всех покупок."""
    return load_purchases()
def delete_purchase(purchase_id: int) -> bool:
    """Удаляет покупку по ID. Возвращает True, если удаление успешно."""
    purchases = load_purchases()
    filtered = [p for p in purchases if p['id'] != purchase_id]
    if len(filtered) == len(purchases):
        raise PurchaseNotFoundError(purchase_id)
    save_purchases(filtered)
    return True

def filter_by_date(purchases, start_date: str, end_date: str):
    """
    Фильтрует список покупок по диапазону дат (включительно).
    start_date, end_date в формате ГГГГ-ММ-ДД.
    """
    # Можно добавить валидацию дат, но для простоты пока без неё
    result = []
    for p in purchases:
        if start_date <= p['date'] <= end_date:
            result.append(p)
    return result

def filter_by_category(purchases, category: str):
    """Фильтрует список покупок по категории (регистронезависимо)."""
    cat_lower = category.lower().strip()
    return [p for p in purchases if p['category'].lower() == cat_lower]