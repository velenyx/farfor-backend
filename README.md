# BACKEND
# Проект FARFOR - Доставка еды
## Запуск приложения:
1) Открываем терминал
2) Устанавливаем виртуальное окружение:
  ```python -m venv venv```
3) Устанавливаем библиотеки:
  ```pip install requirements.txt```
4) Файл .env.dist удалите последние символы .dist. Внутри в поля добавьте свои настройки:
  ```
DB_USER=Пользователь БД
DB_PASS=Пароль БД
DB_NAME=Имя БД
DB_HOST=Хост, если локальный - 127.0.0.1
DB_PORT=5432
```
5) Создаем миграции:
  ```python manage.py makemigrations```
  ```python manage.py migrate```
6) Создаем админа:
  ```python manage.py createsuperuser```
7) Запускаем приложение:
  ```python manage.py runserver```

Приложение будет доступно на http://localhost:8000/
