# NLP Server
Python Flask web service for easy access to multilingual NLP tasks such as language detection, article extraction, entity extraction, sentiment analysis, summarization and more.

NLP Server is intented as an easy way for non-python programming languages to access some of the great NLP libraries that are available in python.

The server is simple to set up and easy to integrate with your programming language of choice.


## Simple Installation
The NLP Server has been tested on Ubuntu, but should work on all flavours of Linux.

```
pip3 install -r requirements.txt
```

### Download Polyglot  mopdels for languages
Polyglot is used for entity extraction, sentiment analysis and embeddings (neighbouring words).

You'll need to download the models for the languages you want to use.

```bash
# For example: English and Norwegian
polyglot download LANG:en
polyglot download LANG:no
```

## Detailed Installation 
INSTALL:
```
sudo apt-get install -Y libicu-dev
sudo apt-get install -y python3-pip

sudo pip3 install pyicu
sudo pip3 install numpy
sudo pip3 install Flask
sudo pip3 install polyglot
sudo pip3 install morfessor
sudo pip3 install langid
sudo pip3 install newspaper3k
sudo pip3 install pycld2
sudo pip3 install gensim
sudo pip3 install spacy
```

## To run:
```
$ nohup python3 nlpserver.py  >logs/nlpserver_out.log 2>logs/nlpserver_errors.log &
```

## Run as a service:
First, install Supervisor if not already installed
```
sudo apt-get update && sudo apt-get install python-setuptools
sudo easy_install supervisor
```
Copy nlpserver.conf to /etc/supervisor/supervisord.conf and edit paths.
Then run this to start the NLPserver:

```
sudo supervisorctl reread
sudo supervisroctl update
sudo supervisorctl nlpserver start
```

## Install Recipe for forge.laravel.com
Add this recipe on Forge and run it as root to install NLPserver.
```
cd /home/forge/
git clone https://github.com/web64/nlpserver.git
chown -R forge:forge /home/forge/nlpserver
cd /home/forge/nlpserver

# python
apt-get install -y python-numpy libicu-dev
apt-get install -y python3-pip
pip3 install -r requirements.txt

# Supervisor
cp nlpserver.conf /etc/supervisor/conf.d
supervisorctl reread
supervisorctl update
supervisorctl start nlpserver
```

## API Endpoints
Endpoint|Method|Parameters|Info|Library
------- | ---- | --------- | -- | -----
/newspaper|GET|url|Article extraction for provided URL|newspaper
/newspaper|POST|html|Article extraction for provided HTML|newspaper
/polyglot|POST|text,lang|Entity extraction and sentiment analysis for provided text|polyglot
/language|GET,POST|text|Language detection from provided text|langid
/embeddings|GET|word|Embeddinga: neighbouring words|polyglot
/summarize|POST|text|Summarization of long text|gensim
/spacy/entities|POST|text,lang|Entity extraction for provided text in guiven language|SpaCy

## Contribute
If you are familiar with NLP or Python, please let us know how this project can be improved!

## Future tasks
- [ ] News Classification
- [ ] Translation
- [ ] Use more production ready webserver than Flask's built in server
