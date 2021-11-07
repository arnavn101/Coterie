# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

ENV APP_HOME /app
WORKDIR $APP_HOME



RUN apt-get update && apt-get install -y git
RUN apt-get install build-essential -y

RUN useradd -l -u 1001 -ms /bin/bash localuser

USER localuser
WORKDIR /home/localuser

# Install dependencies.
COPY requirements.txt .

RUN pip install -U pip && pip install  -U -r requirements.txt

# Copy local code to the container image.
COPY . .

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8000

# Setting this ensures print statements and log messages
# promptly appear in Cloud Logging.
ENV PYTHONUNBUFFERED TRUE

# Run the web service on container startup
RUN python manage.py migrate
CMD exec python manage.py runserver 0.0.0.0:8000
