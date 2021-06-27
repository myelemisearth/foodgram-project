FROM ubuntu:latest
WORKDIR /code
COPY . .
RUN pip3 install -r requirements.txt
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
