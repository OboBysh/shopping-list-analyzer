# shoppingcli/analytics.py
"""Аналитические функции для списка покупок."""

from collections import Counter

def total_spent(purchases):
    """Общая сумма расходов."""
    return sum(p['price'] for p in purchases)

def top_items(purchases, n=3):
    """
    Топ n самых часто покупаемых товаров (по названию).
    Возвращает список кортежей (название, количество).
    """
    if not purchases:
        return []
    counter = Counter(p['name'] for p in purchases)
    return counter.most_common(n)

def spending_by_category(purchases):
    """Распределение трат по категориям: категория -> сумма."""
    result = {}
    for p in purchases:
        cat = p['category']
        result[cat] = result.get(cat, 0) + p['price']
    return result

def daily_expenses(purchases):
    """Динамика расходов во времени: дата -> сумма за день."""
    daily = {}
    for p in purchases:
        date = p['date']
        daily[date] = daily.get(date, 0) + p['price']
    # Сортировка по дате для удобства
    return dict(sorted(daily.items()))