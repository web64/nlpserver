# NLP Server
Python Flask web service for eacy access to multi-linguial NLP tasks.

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
sudo pip3 install summa
sudo pip3 install pattern
```

## To run:
```
$ nohup python3 nlpserver.py  >nlpserver_out.log 2>nlpserver_errors.log &
```


## Future tasks
- [ ] Add SpaCy support
- [ ] Use more production ready webserver than Flask's built in server
