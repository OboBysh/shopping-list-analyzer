# shoppingcli/cli.py
"""Консольный интерфейс для управления покупками."""

from .logic import add_purchase, get_all_purchases, delete_purchase, filter_by_date, filter_by_category
from .exceptions import ValidationError, PurchaseNotFoundError, StorageError
from .analytics import total_spent, top_items, spending_by_category, daily_expenses


def print_purchases(purchases):
    """Выводит список покупок в табличном виде."""
    if not purchases:
        print("Нет покупок.")
        return
    print("\n" + "-" * 70)
    print(f"{'ID':<4} {'Название':<20} {'Категория':<12} {'Дата':<12} {'Цена':<8}")
    print("-" * 70)
    for p in purchases:
        print(f"{p['id']:<4} {p['name']:<20} {p['category']:<12} {p['date']:<12} {p['price']:<8.2f}")
    print("-" * 70 + "\n")


def show_statistics(purchases):
    """Выводит всю статистику."""
    if not purchases:
        print("Нет данных для статистики.")
        return
    print("\n=== СТАТИСТИКА ===")
    print(f"Общая сумма расходов: {total_spent(purchases):.2f} руб.")

    print("\nТоп самых покупаемых товаров:")
    top = top_items(purchases, 5)
    for i, (name, count) in enumerate(top, 1):
        print(f"  {i}. {name} — {count} раз(а)")

    print("\nРаспределение трат по категориям:")
    for cat, amount in spending_by_category(purchases).items():
        print(f"  {cat}: {amount:.2f} руб.")

    print("\nДинамика расходов по дням:")
    for date, amount in daily_expenses(purchases).items():
        print(f"  {date}: {amount:.2f} руб.")
    print()


def main():
    while True:
        print("\n=== МЕНЕДЖЕР ПОКУПОК ===")
        print("1. Добавить покупку")
        print("2. Показать все покупки")
        print("3. Показать покупки за период (фильтр по дате)")
        print("4. Показать покупки по категории")
        print("5. Статистика")
        print("6. Удалить покупку по ID")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == '1':
            try:
                name = input("Название товара: ").strip()
                category = input("Категория: ").strip()
                date = input("Дата (ГГГГ-ММ-ДД): ").strip()
                price = float(input("Цена: ").strip())
                new_id = add_purchase(name, category, date, price)
                print(f"✓ Покупка добавлена с ID {new_id}.")
            except ValidationError as e:
                print(f"Ошибка: {e}")
            except ValueError:
                print("Ошибка: цена должна быть числом.")

        elif choice == '2':
            purchases = get_all_purchases()
            print_purchases(purchases)

        elif choice == '3':
            start = input("Начальная дата (ГГГГ-ММ-ДД): ").strip()
            end = input("Конечная дата (ГГГГ-ММ-ДД): ").strip()
            try:
                # простая проверка формата (необязательно)
                purchases = get_all_purchases()
                filtered = filter_by_date(purchases, start, end)
                print_purchases(filtered)
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == '4':
            cat = input("Категория: ").strip()
            purchases = get_all_purchases()
            filtered = filter_by_category(purchases, cat)
            print_purchases(filtered)

        elif choice == '5':
            purchases = get_all_purchases()
            show_statistics(purchases)

        elif choice == '6':
            try:
                pid = int(input("ID покупки для удаления: ").strip())
                delete_purchase(pid)
                print(f"✓ Покупка с ID {pid} удалена.")
            except PurchaseNotFoundError as e:
                print(f"Ошибка: {e}")
            except ValueError:
                print("Ошибка: ID должно быть числом.")

        elif choice == '0':
            print("До свидания!")
            break

        else:
            print("Неверный выбор, попробуйте снова.")