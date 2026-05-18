# Shopping List Analyzer

Консольное приложение для учёта и анализа расходов на покупки.

## Возможности

- Добавление покупок (название, категория, дата, цена)
- Просмотр всех покупок с фильтрацией по категории или диапазону дат
- Статистика:
  - Общая сумма расходов
  - Топ самых часто покупаемых товаров
  - Распределение трат по категориям
  - Расходы по дням
- Сохранение данных в JSON-файл (shopping_data.json)
- Удаление покупок по ID

## Установка и запуск

1. Клонируйте репозиторий:
   git clone https://github.com/OboBysh/shopping-list-analyzer.git
   cd shopping-list-analyzer
2. Создайте виртуальное окружение:
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
3. Установите зависимости:
   pip install -r requirements.txt
4. Запустите приложение:
   python main.py
Тестирование
   pytest tests/
Структура проекта
-shoppingcli/ – основной пакет
   -cli.py – интерфейс командной строки
   -logic.py – бизнес-логика
   -storage.py – работа с JSON
   -analytics.py – расчёты статистики
   -exceptions.py – пользовательские исключения
-tests/ – модульные тесты
-main.py – точка входа
Лицензия MIT
