# shoppingcli/exceptions.py
"""Пользовательские исключения для приложения."""

class StorageError(Exception):
    """Ошибка при работе с файлом данных (чтение/запись)."""
    pass

class ValidationError(Exception):
    """Ошибка валидации ввода (пустое название, отрицательная цена, неверный формат даты)."""
    pass

class PurchaseNotFoundError(Exception):
    """Покупка с указанным ID не найдена."""
    def __init__(self, purchase_id: int):
        super().__init__(f"Покупка с ID {purchase_id} не найдена.")
        self.purchase_id = purchase_id