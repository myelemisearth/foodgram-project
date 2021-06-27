FROM ubuntu

WORKDIR /code
COPY . .
RUN sudo apt-get update || sudo apt-get install python3 python3-pip -y
RUN pip3 install -r requirements.txt
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
