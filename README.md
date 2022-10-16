# URL Shortener

  

## Description

  

URL Shortener API allows you to generate new URL for some website either to shorten or hide the original URL.

  

## Built with

* Django Rest Framework

* Docker

* PostgreSQL

  

## Getting Started Dev

  

In order to use this API: clone this repository to your machine, in terminal go to project directory and:

```

sudo chmod +x ./app/entrypoint.sh

docker compose up -d --build

docker compose exec web python manage.py migrate --noinput

```

## Usage Dev

After you started app you can follow this link http://localhost:8000/shorten/ there you can paste some url and get shortened version of it.

There are also two other endpoints:

http://localhost:8000/shortened-urls-count/ - displays information about how many urls were shortened using this API

http://localhost:8000/the-most-popular/ - displays URL's sorted in descending order by their popularity among users

  

## Getting Started Prod

  

In order to use this API: clone this repository to your machine, in terminal go to project directory and:

Create .env.prod file and fill it with data as shown below with changing marked variables:

```

DEBUG=1

SECRET_KEY=change_me

DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

SQL_ENGINE=django.db.backends.postgresql

SQL_DATABASE=url_shortener_prod

SQL_USER=change_me

SQL_PASSWORD=change_me

SQL_HOST=db

SQL_PORT=5432

DATABASE=postgres

HOST_URL=https://localhost/

  

```

Create .env.prod.db file and fill it with data as shown below with changing marked variables:

```

POSTGRES_USER=change_me

POSTGRES_PASSWORD=change_me

POSTGRES_DB=url_shortener_prod

```

  

Then run this commands in root directory of project

```

sudo chmod +x ./app/entrypoint.prod.sh

docker compose -f docker-compose.prod.yml up -d --build

docker compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic

```

## Usage Prod

After you started app you can follow this link https://localhost/shorten/ there you can paste some url and get shortened version of it.

There are also two other endpoints:

https://localhost/shortened-urls-count/ - displays information about how many urls were shortened using this API

https://localhost/the-most-popular/ - displays URL's sorted in descending order by their popularity among users


## Scaling

You can scale gunicorn workers by changing return value of **max_workers** function in gunicorn.conf.py file

```

def max_workers():

return cpu_count()

```