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

# Install dependencies
RUN apt-get -y install pkg-config && \
 	apt-get -y install -y python-numpy libicu-dev && \
 	apt-get -y install -y python3-pip && \
 	python3 -m pip install -r requirements.txt

# Download language models
RUN polyglot download LANG:en && \
 	polyglot download LANG:es 

RUN python3 -m spacy download en && \
	python3 -m spacy download es && \
	python3 -m spacy download xx

# Set supervisor config
COPY nlpserver.conf /etc/supervisor/conf.d
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
 
EXPOSE 6400