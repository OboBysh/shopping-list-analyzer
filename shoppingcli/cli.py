# shoppingcli/cli.py
"""Консольный интерфейс пользователя."""

from datetime import datetime
from .logic import (
    add_purchase, get_all_purchases, delete_purchase,
    filter_by_date, filter_by_category
)
from .analytics import total_spent, top_items, spending_by_category, daily_expenses
from .exceptions import ValidationError, PurchaseNotFoundError, StorageError

def print_separator():
    print("-" * 50)

def print_purchase(p):
    """Вывод одной покупки в читаемом виде."""
    print(f"ID: {p['id']} | {p['date']} | {p['name']:15} | {p['category']:12} | {p['price']:8.2f} руб.")

def show_purchases(purchases):
    """Вывод списка покупок."""
    if not purchases:
        print("📭 Нет покупок.")
        return
    print_separator()
    print(f"{'ID':<4} {'Дата':<12} {'Название':<15} {'Категория':<12} {'Цена, руб':<10}")
    print_separator()
    for p in purchases:
        print(f"{p['id']:<4} {p['date']:<12} {p['name']:<15} {p['category']:<12} {p['price']:<10.2f}")
    print_separator()

def add_purchase_interactive():
    """Интерактивное добавление покупки."""
    print("\n--- Добавление покупки ---")
    name = input("Название товара: ").strip()
    if not name:
        print("❌ Название не может быть пустым.")
        return
    category = input("Категория (например, Продукты, Транспорт): ").strip()
    if not category:
        print("❌ Категория не может быть пустой.")
        return
    date_str = input("Дата (ГГГГ-ММ-ДД): ").strip()
    try:
        price = float(input("Цена (руб): ").strip())
    except ValueError:
        print("❌ Цена должна быть числом.")
        return
    try:
        purchase_id = add_purchase(name, category, date_str, price)
        print(f"✅ Покупка добавлена с ID {purchase_id}.")
    except ValidationError as e:
        print(f"❌ Ошибка: {e}")
    except StorageError as e:
        print(f"❌ Ошибка хранения: {e}")

def delete_purchase_interactive():
    """Удаление покупки по ID."""
    print("\n--- Удаление покупки ---")
    try:
        pid = int(input("ID покупки для удаления: "))
    except ValueError:
        print("❌ ID должно быть целым числом.")
        return
    try:
        delete_purchase(pid)
        print(f"✅ Покупка с ID {pid} удалена.")
    except PurchaseNotFoundError as e:
        print(f"❌ {e}")
    except StorageError as e:
        print(f"❌ Ошибка хранения: {e}")

def view_purchases_interactive():
    """Просмотр покупок с возможностью фильтрации."""
    purchases = get_all_purchases()
    if not purchases:
        print("📭 Нет покупок.")
        return
    print("\n--- Просмотр покупок ---")
    print("Показать: 1 - все, 2 - по категории, 3 - по диапазону дат")
    choice = input("Ваш выбор: ").strip()
    if choice == "2":
        cat = input("Введите категорию: ").strip()
        filtered = filter_by_category(purchases, cat)
        print(f"\nПокупки в категории '{cat}':")
        show_purchases(filtered)
    elif choice == "3":
        start = input("Начальная дата (ГГГГ-ММ-ДД): ").strip()
        end = input("Конечная дата (ГГГГ-ММ-ДД): ").strip()
        try:
            datetime.strptime(start, "%Y-%m-%d")
            datetime.strptime(end, "%Y-%m-%d")
        except ValueError:
            print("❌ Неверный формат даты. Используйте ГГГГ-ММ-ДД.")
            return
        filtered = filter_by_date(purchases, start, end)
        print(f"\nПокупки с {start} по {end}:")
        show_purchases(filtered)
    else:
        show_purchases(purchases)

def stats_interactive():
    """Вывод статистики."""
    purchases = get_all_purchases()
    if not purchases:
        print("📭 Нет данных для статистики.")
        return
    print("\n--- Статистика расходов ---")
    print(f"💰 Общая сумма: {total_spent(purchases):.2f} руб.")
    print("\n📊 Топ самых частых товаров:")
    top = top_items(purchases, 5)
    if top:
        for name, count in top:
            print(f"   {name}: {count} раз(а)")
    else:
        print("   Нет данных")
    print("\n📂 Распределение по категориям:")
    by_cat = spending_by_category(purchases)
    for cat, amount in by_cat.items():
        print(f"   {cat}: {amount:.2f} руб.")
    print("\n📅 Расходы по дням:")
    daily = daily_expenses(purchases)
    for date, amount in sorted(daily.items()):
        print(f"   {date}: {amount:.2f} руб.")

def main():
    """Главное меню."""
    while True:
        print("\n" + "=" * 40)
        print("        МЕНЕДЖЕР ПОКУПОК")
        print("=" * 40)
        print("1. Добавить покупку")
        print("2. Просмотреть покупки")
        print("3. Статистика")
        print("4. Удалить покупку")
        print("5. Выход")
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            add_purchase_interactive()
        elif choice == "2":
            view_purchases_interactive()
        elif choice == "3":
            stats_interactive()
        elif choice == "4":
            delete_purchase_interactive()
        elif choice == "5":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор, попробуйте снова.")