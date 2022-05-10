# Use the official image as a parent image.
FROM python:3.8.5-slim-buster

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install -y supervisor

# Set the working directory.
WORKDIR /usr/src
RUN git clone https://github.com/web64/nlpserver.git
WORKDIR /usr/src/nlpserver
RUN git branch fastapi

# Install dependencies
RUN apt-get -y install pkg-config && \
 	apt-get -y install -y python-numpy libicu-dev && \
 	apt-get -y install -y python3-pip && \
 	python3 -m pip install -r requirements.txt

# Download language models
RUN polyglot download LANG:en

RUN python3 -m spacy download en
CMD ["uvicorn", "nlpserver:app"]
#EXPOSE 8000
