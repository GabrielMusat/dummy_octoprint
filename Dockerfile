FROM python:3.7

WORKDIR /home/pi/.octoprint

COPY . /home/pi/.octoprint/

RUN pip install -r requeriments.txt