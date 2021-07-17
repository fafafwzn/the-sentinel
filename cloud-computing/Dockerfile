# Use the official latest ubuntu image.
# https://hub.docker.com/_/ubuntu
FROM ubuntu:latest

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV DEBIAN_FRONTEND=noninteractive 

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN apt-get update -y
RUN apt-get install python3.9 python3-pip -y
RUN pip3 install -r requirements.txt
RUN gdown https://drive.google.com/uc?id=1QYh8lid_u052BKXMxKiHrX1TVvsEso11
RUN python3 -m zipfile -e the_sentinel.zip /
RUN rm the_sentinel.zip

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --workers 1 --threads 8 --timeout 300 --bind 0.0.0.0:8080 main:app