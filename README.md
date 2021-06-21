# Test App

## Build
Соберет образы: **redis, postgresql, fastapi, nginx** 

    $ cd deploy
    $ docker-compose up --build


## Access to paths

* Основной сайт доступен по url - **http://0.0.0.0:8080/users**
* Авторизация - **http://0.0.0.0:8080/login**
* Регистрация - **http://0.0.0.0:8080/singup**
* Интерактивная документация по всем линкам доступен по url - **http://0.0.0.0:8000/docs**

## Stack
* FastApi
* SQLAlchemy
* PostgreSQL
* JS(JQuery)


## Other
Реализацию 2х задач обьеденил в одном сервисе. 
Загрузка начальный данных в базу происходит при сборки контейнера.
Файл дампа базы лежит в **deploy/postgresql/init**.
