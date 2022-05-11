# Use the official image as a parent image.
FROM python:3.8.5-slim-buster

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install -y supervisor && \
	apt-get install -y tk

# Set the working directory.
WORKDIR /usr/src
WORKDIR /usr/src/nlpserver

COPY requirements.txt /usr/src/nlpserver/
COPY . /usr/src/nlpserver/

# Install dependencies
RUN apt-get -y install pkg-config && \
 	apt-get -y install -y python-numpy libicu-dev && \
 	apt-get -y install -y python3-pip && \
 	python3 -m pip install -r requirements.txt

CMD ["uvicorn", "nlpserver:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80
