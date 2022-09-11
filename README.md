# Foodgram - Продуктовый помощник

## Описание проекта

Foodgram это ресурс для публикации рецептов.
Пользователи могут создавать свои рецепты, читать рецепты других пользователей, подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок и загружать его.

## Как запустить проект локально:
Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone https://github.com/Starponi/foodgram-project-react 
cd foodgram-project-react
```
Cоздать и активировать виртуальное окружение:
```bash
python -m venv env
source env/bin/activate
```
Создать суперпользователя: 
```bash
docker-compose exec web python manage.py createsuperuser
```

Перейти в директирию и установить зависимости из файла requirements.txt:
```bash
cd backend/
pip install -r requirements.txt
```
Выполните миграции:
```bash
python manage.py migrate
```
Запустите сервер:
```bash
python manage.py runserver
```
## Запуск проекта в Docker контейнере
Запустите docker compose:
```bash
docker-compose up -d --build
```
Примените миграции:
```bash
docker-compose exec backend python manage.py migrate
```
Создайте администратора
```bash
docker-compose exec backend python manage.py createsuperuser
```
Соберите статику:
```bash
docker-compose exec backend python manage.py collectstatic --noinput
```
