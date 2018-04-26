# NLP Server
Python Flask web service for easy access to multilingual NLP tasks.

## Simple Installation
```
pip3 install -r requirements.txt
```

### Download Polyglot  mopdels for languages
```
polyglot download LANG:no
polyglot download LANG:en
```

## Detailed Installation 
INSTALL:
```
sudo apt-get install -Y python-numpy libicu-dev
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

## Future tasks
- [ ] Add SpaCy support
- [ ] Use more production ready webserver than Flask's built in server
