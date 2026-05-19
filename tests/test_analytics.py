# tests/test_analytics.py
from shoppingcli.analytics import total_spent, top_items, spending_by_category, daily_expenses

def test_total_spent():
    purchases = [
        {'price': 100},
        {'price': 200},
    ]
    assert total_spent(purchases) == 300

def test_top_items():
    purchases = [
        {'name': 'Молоко'},
        {'name': 'Хлеб'},
        {'name': 'Молоко'},
        {'name': 'Масло'},
    ]
    top = top_items(purchases, 2)
    assert top == [('Молоко', 2), ('Хлеб', 1)]

def test_spending_by_category():
    purchases = [
        {'category': 'Продукты', 'price': 100},
        {'category': 'Транспорт', 'price': 200},
        {'category': 'Продукты', 'price': 50},
    ]
    result = spending_by_category(purchases)
    assert result == {'Продукты': 150, 'Транспорт': 200}

def test_daily_expenses():
    purchases = [
        {'date': '2025-03-10', 'price': 100},
        {'date': '2025-03-10', 'price': 50},
        {'date': '2025-03-11', 'price': 200},
    ]
    result = daily_expenses(purchases)
    assert result == {'2025-03-10': 150, '2025-03-11': 200}
