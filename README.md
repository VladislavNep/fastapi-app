# Test App
В новых версиях firefox не корректно отрабатывает запросы с nginx из-за новой политики безопасности.
Google Chrome норм обрабатывает)

## Build
Соберет образы: **redis, postgresql, fastapi, nginx** 

    $ cd deploy
    $ docker-compose up --build


## Access to paths

* Основной сайт доступен по url - **http://0.0.0.0:8080/users**
* Авторизация - **http://0.0.0.0:8080/login**
* Регистрация - **http://0.0.0.0:8080/singup**
* Интерактивная документация по всем линкам доступен по url - **http://0.0.0.0:8000/docs**
* Для Авторизации использовать следующие данные:

        email: alar@gmail.com
        password: 123456789

## Stack
* FastApi
* SQLAlchemy
* PostgreSQL
* JS(JQuery)


## Other
Реализацию 2х задач обьеденил в одном сервисе. 
Загрузка начальный данных в базу происходит при сборки контейнера.
Файл дампа базы лежит в **deploy/postgresql/init**.


## Demo
![alt](demo.gif)