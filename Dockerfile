FROM python:3.8.5
WORKDIR /code
COPY . .
RUN sed -i 's/main/main contrib/g' /etc/apt/sources.list && apt-get update && apt-get install ttf-mscorefonts-installer -y
RUN pip3 install -r requirements.txt
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
