# Тестовое задание по aiohttp и aiopg

## Подготовка среды

Необходимо форкнуть данный репозиторий и все работы проводить в собственном форке.

Необходимо устновить зависимости и настроить базу данных:

    python3 -m venv venv
    pip install -e .
    sudo -u postgres psql -c "CREATE USER att_user WITH PASSWORD 'att_pass';"
    sudo -u postgres psql -c "CREATE DATABASE att_db WITH OWNER = att_user;"
    sudo -u postgres psql -c "CREATE EXTENSION btree_gist;" att_db
    sudo -u postgres psql -c "CREATE EXTENSION pgcrypto;" att_db
    alembic upgrade head

Затем можно запустить веб-сервер:

    att-server --db-url=postgres://att_user:att_pass@localhost/att_db

и попробовать сделать запрос к нему:

    curl http://localhost:8000/login -H 'Content-Type: application/json' -d '{"login": "bob", "password": "secrets"}'

Если в результате получен ответ вроде

    {"user_id": "ff73cccd-dd14-4eb7-8aa8-7059f26239b8"}

значит всё работает.


## Задания

Все изменения необходимо оформить отдельными коммитами.

* Добавить опцию для указания интерфейса и порта, на котором будет работать
вебсервер (например `--listen 0.0.0.0:8080`).
* Вынести функции обработки запросов (`login`, `user_groups` и т.д) в отдельный модуль.
* Добавить метод для добавления пользователя (`/signup`).
* Написать юнит-тест для функции `make_login_response` используя `pytest`.
* Добавить таблицы для групп пользователей и связи пользователей с группами (пользователь может входить сразу в несклько групп), создать скрипт миграции при помощи `alembic revision --autogenerate -m "Added group table"`.
* Добавить методы для работы с группами: создание групп, добавление и удаление пользователя из групп.
* Добавить метод для получения сообщений пользователем по WebSocket'ам (`/listen/{user_id}`), для проверки этого метода можно использовать [wscat](https://github.com/websockets/wscat) (`wscat --connect ws://localhost:8000/listen/ff73cccd-dd14...`) или его аналог.
* Добавить ответный метод `/broadcast/{group}`, который будет рассылать сообщение (JSON объект) всем подключеным в данный момент пользователям из конкретной группы.

Дополнительные юнит и интеграционные тесты будут плюсом (для интеграционных тестов можно использовать [pytest-postgresql](https://pypi.org/project/pytest-postgresql/)).

Для получения обратной связи нужно сделать пулл реквест в данный репозиторий.

## Ссылки на документацию

* [aiohttp documentation](https://aiohttp.readthedocs.io/en/stable/)
* [aiopg documentation](https://aiopg.readthedocs.io/en/stable/)
* [alembic documentation](https://alembic.sqlalchemy.org/en/latest/)
* [click documentation](https://click.palletsprojects.com/en/7.x/)
* [sqlalchemy documentation](https://docs.sqlalchemy.org/en/13/)
