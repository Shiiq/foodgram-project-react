## foodgram-project  
![main](https://github.com/Shiiq/foodgram-project-react/actions/workflows/foodgram-backend.yml/badge.svg)  
Учебный проект Я.Практикум. Кулинарный сайт с возможностью публикации своих рецептов, просмотров рецептов других авторов. Реализована аутентификация и авторизация, понравившиеся рецепты можно добавлять в избранное, кидать в корзину покупок, с последующей возможностью скачивания списка покупок по ингредиентам.
---
Сайт доступен по адресу: ~~51.250.99.184~~ **(на данный момент неактивен)**  
Для доступа в админ-зону используйте логин _main@main.ru_ и пароль _123_.  

#### Как запустить проект:  
скачать репозиторий  
  ```
  git clone https://github.com/Shiiq/foodgram-project-react.git
  ```  
перейти в папку с проектом  
  ```
  cd foodgram-project-react
  ```   
установить и активировать виртуальное окружение  
  ```
  python -m venv venv
  source venv/Scripts/activate
  ```  
установить зависимости из файла requirements.txt  
  ```
  pip install -r path/to/requirements.txt
  ```
в директории проекта, в папке **infra** создать файл _.env_ и заполнить по образцу:
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
для локального запуска проекта необходимо в файле **nginx.conf** поменять значение параметра _server_name_ на _localhost_  
приступаем к сборке и запуску контейнеров
  ```
  docker-compose up -d --build
  ```
после сборки и запуска контейнеров необходимо выполнить последовательно команды:
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
  4. Для дальнейшей работы с сайтом на главной странице будет предложено зарегистрироваться.  
  После чего появится возможность публиковать свои рецепты, подписываться на других авторов, добавлять в избранное и создавать списки покупок.
  5. Если необходимо, то сервер можно остановить;
  ```
  docker-compose stop web
  ```
  6. Либо перезагрузить;
  ```
  docker-compose restart web
  ```
- после запуска сервера будут доступны к просмотру:  
[страница регистрации](http://localhost/signup)  
[страница логина](http://localhost/signin)  
[главная страница проекта](http://localhost/recipes)  
[справка апи проекта и примеры запросов](http://localhost/api/docs/)

### Автор: Киряков Петр, 2022
