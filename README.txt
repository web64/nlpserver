# README-web64
# pip3 install -r requirements.txt

To run:
$ nohup python3 nlpserver.py  >nlpserver_out.log 2>nlpserver_errors.log &

INSTALL:
sudo apt-get install -Y python-numpy libicu-dev
sudo apt-get install -y python3-pip

sudo pip3 install pyicu
sudo pip3 install numpy
sudo pip3 install Flask
sudo pip3 install polyglot
sudo pip3 install morfessor
#sudo pip3 install flask-mysql
sudo pip3 install langid
sudo pip3 install newspaper3k
sudo pip3 install pycld2
sudo pip3 install summa
sudo pip3 install pattern

# Download Pologloy mopdels for languages
polyglot download LANG:no
polyglot download LANG:en








# polyglot download embeddings2.no
# polyglot download ner2.no

# https://github.com/aboSamoor/pycld2 - Compact Language Detector 2
$ git clone http://github.com/abosamoor/pycld2.git
$ cd pycld2
$ sudo ./setup.py install


wget https://github.com/saffsd/langid.py/raw/master/langid/langid.py


