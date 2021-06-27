![example workflow](https://github.com/myelemisearth/foodgram-project/actions/workflows/foodgram_workflow.yaml/badge.svg)
# About Foodgram
It is a service where you can make your own recipes, follow other users, add recipes to your favorite recipes, add recipes to basket and download list of summary ingredients with their amount.

## Installation dependencies
For installing components you should have machine on linux and docker [docker](https://www.docker.com/).

[HOWTO](https://docs.docker.com/engine/install/) for installing docker.

After installing docker enable service and add it to autorun.

```bash
sudo systemctl enable docker && sydo systemctl restart docker
```

## Installation Foodgram

You should download project from a [github link](https://github.com/myelemisearth/foodgram-project), and running commands bellow.


If you don't have a [github](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) on a work machine please install it.

```bash
git clone https://github.com/myelemisearth/foodgram-project

cd foodgram-project

sudo docker-compose up -d --build
```

## Database form

After installing you should make migrations for database, createsuperuser and collect static for nginx non-interactive pages.

```bash
sudo docker-compose exec web python3 manage.py makemigrations recipes --noinput

sudo docker-compose exec web python3 manage.py migrate --noinput

sudo docker-compose exec web python3 manage.py createsuperuser

sudo docker-compose exec web python3 manage.py collectstatic --no-input
```

## Finish

The project has an existing content of ingredients.

For add content in your database you could running command bellow.

```bash
sudo docker-compose exec web python3 manage.py import_ingredients templates/ingredients/ingredients.json
```
For checking real service you could refer to [link](http://myrecipes.tk/)