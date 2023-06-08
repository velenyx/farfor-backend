# BACKEND
# Проект FARFOR - Доставка еды
## Запуск приложения:
1) Открываем терминал
2) Устанавливаем виртуальное окружение:
  ```python -m venv venv```
3) Устанавливаем библиотеки:
  ```pip install requirements.txt```
4) Создаем миграции:
  ```python manage.py makemigrations```
  ```python manage.py migrate```
5) Создаем админа:
  ```python manage.py createsuperuser```
6) Запускаем приложение:
  ```python manage.py runserver```

Приложение будет доступно на http://localhost:8000/
