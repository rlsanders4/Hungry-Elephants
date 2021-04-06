# pull the official base image
FROM python:3.8-slim-buster

# Make a new directory to put our code in.
RUN mkdir /code

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip 
COPY ./requirements.txt /code
RUN pip install -r requirements.txt

# copy project
COPY ./server_controller /code/server_controller
COPY ./website /code/website
COPY ./db /code/db
COPY ./run.sh /code/run.sh

EXPOSE 8000

CMD ["bash", "./run.sh"]
