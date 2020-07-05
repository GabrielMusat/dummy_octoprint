FROM python:3.7

WORKDIR /home/pi/dummy_octoprint

COPY . /home/pi/dummy_octoprint/

RUN pip install -r requeriments.txt