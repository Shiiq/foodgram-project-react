# foodgram-project
![main](https://github.com/Shiiq/foodgram-project-react/actions/workflows/foodgram-backend.yml/badge.svg)  
Сайт доступен по адресу: **51.250.99.184** (на данный момент недоступен)  
Для доступа в админ-зону используйте логин _main@main.ru_ и пароль _123_.  

Как запустить проект:
- скачать репозиторий ```git clone https://github.com/Shiiq/foodgram-project-react.git```
- скачать образ Docker ```docker pull https://hub.docker.com/repository/docker/peterkiriakov/foodgram```
- в директории проекта, в папке **infra** создать файл _.env_ и заполнить по образцу:
  ```
  ALLOWED_HOSTS="['*']"
  DB_ENGINE=django.db.backends.postgresql
  POSTGRES_DB=fake_postgres
  POSTGRES_USER=fake_user
  POSTGRES_PASSWORD=fake_password
  DB_HOST=fake_host
  DB_PORT=1234
  SECRET_KEY='la926#41*92@as)1_d0'
  ```
- собрать и запустить контейнеры командой ```docker-compose up -d --build```
- после сборки и запуска контейнеров необходимо выполнить последовательно команды:
  1. Запустить миграции;
  ```
  docker-compose exec web python manage.py makemigrations users
  docker-compose exec web python manage.py migrate users
  docker-compose exec web python manage.py makemigrations recipes
  docker-compose exec web python manage.py migrate recipes
  docker-compose exec web python manage.py migrate
  ```
  2. Собрать статику проекта;
  ```
  sudo docker-compose exec web python3 manage.py collectstatic --no-input
  ```
  3. Заполнить базу данных проекта списком тегов и ингредиентов;
  ```
  docker-compose exec web python manage.py importcsv tags.csv Tag
  docker-compose exec web python manage.py importcsv ingredients.csv Ingredient
  ```
  5. Для дальнейшей работы с сайтом на главной странице будет предложено зарегистрироваться.  
  После чего появится возможность публиковать свои рецепты, подписываться на других авторов, добавлять в избранное и создавать списки покупок.
  6. Если необходимо, то сервер можно остановить;
  ```
  docker-compose stop web
  ```
  5. Либо перезагрузить;
  ```
  docker-compose restart web
  ```
- после запуска сервера будут доступны к просмотру:  
[страница регистрации](http://51.250.99.184/signup)  
[страница логина](http://51.250.99.184/signin)  
[главная страница проекта](http://51.250.99.184/recipes)  
[справка апи проекта и примеры запросов](http://51.250.99.184/api/docs/)

### Автор: Киряков Петр, 2022
