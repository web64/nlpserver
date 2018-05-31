# NLP Server
Python 3 Flask web service for easy access to multilingual NLP tasks such as language detection, article extraction, entity extraction, sentiment analysis, summarization and more.

NLP Server is intented as an easy way for non-python programming languages to access some of the great NLP libraries that are available in python.

The server is simple to set up and easy to integrate with your programming language of choice.


## Simple Installation
The NLP Server has been tested on Ubuntu, but should work on all Linux flavours.
```
pip3 install -r requirements.txt
```

### Download Polyglot  models for languages
Polyglot is used for entity extraction, sentiment analysis and embeddings (neighbouring words).

You'll need to download the models for the languages you want to use.

```bash
# For example: English and Norwegian
polyglot download LANG:en
polyglot download LANG:no
```
The root api endpoint will list installed Polyglot language modules: http://localhost:6400/

### Download SpaCy models for entity extraction (NER)
If you want to use the /spacy/entities endpoint for article extraction you need to download the models for the languages you want to use
```bash
# For example English, Spanish and Multi-Language
python -m spacy download en
python -m spacy download es
python -m spacy download xx
```


### Detailed Installation 
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
sudo pip3 install readability-lxml
sudo pip3 install BeautifulSoup4
```
The root api endpoint will list missing python modules: http://localhost:6400/

## To run:
```
$ nohup python3 nlpserver.py  >logs/nlpserver_out.log 2>logs/nlpserver_errors.log &
```

## API Endpoints
Endpoint|Method|Parameters|Info|Library
------- | ---- | --------- | -- | ----- 
/status|GET| |List installed Polyglot language models and  missing python packages |
/newspaper|GET|url|Article extraction for provided URL|newspaper
/newspaper|POST|html|Article extraction for provided HTML|newspaper
/readability|GET|url|Article extraction for provided URL|readability-lxml
/readability|POST|html|Article extraction for provided HTML|readability-lxml
/polyglot/entities|POST|text,lang|Entity extraction and sentiment analysis for provided text|polyglot
/polyglot/sentiment|POST|text,lang|Sentiment analysis for provided text|polyglot
/polyglot/neighbours|GET|word,lang|Embeddings: neighbouring words|polyglot
/langid|GET,POST|text|Language detection for provided text|langid
/gensim/summarize|POST|text|Summarization of long text|gensim
/spacy/entities|POST|text,lang|Entity extraction for provided text in given language|SpaCy

## PHP & Laravel clients
A PHP library and Laraval package is available:
* https://github.com/web64/php-nlp-client
* https://github.com/web64/laravel-nlp


## Usage
For API responses see /response_examples/ directory.

### /newspaper - Article & Metadata Extraction
Returns article text, authors, main image, publish date and meta-data for given url or HTML.

#### From URL: 
GET /newspaper?url=https://github.com/web64/nlpserver
```bash
curl http://localhost:6400/newspaper?url=https://github.com/web64/nlpserver
```

#### From HTML:
POST /newspaper [html="<html>....</html>"]
```bash
curl -d "html=<html>...</html>" http://localhost:6400/newspaper
```

### /langid - Language Detection
GET|POST /langid?text=what+language+is+this

```bash
curl http://localhost:6400/langid?text=what+language+is+this
```

Returns language code of provided text
```json
langid: {
language: "en",
score: -42.31864953041077
}
```

### Entity Extraction & Sentiment Analysis
### POST /polyglot/entities [params: text]
```bash
curl -d "text=The quick brown fox jumps over the lazy dog" http://localhost:6400/polyglot/entities
```

### Sentiment Analysis
### POST /polyglot/sentiment [params: text, lang (optional)]

```bash
curl -d "text=This is great!" http://localhost:6400/polyglot/sentiment
```
```json
{
  "message": "Sentiment Analysis API - POST only",
  "sentiment": 1.0,
}
```


### /spacy/entities - SpaCy Entiry Extraction
Note: You'll need to have downloaded the language models for the language you are using

### POST /spacy/entities [params: text, lang]
```bash
curl -d "text=President Donald Trump says dialogue with North Korea is productive" http://localhost:6400/spacy/entities
```

```json
"entities": {
    "GPE": {
      "0": "North Korea"
    },
    "PERSON": {
      "0": "Donald Trump"
    }
  }
```

###  Text summariztion
### POST /gensim/summarize [params: text, word_count (optional)]
Generates summary for long text. Size of summary by adding a word_count parameter with the maximum number of words in summary.


## Neighbouring words
### GET /polyglot/neighbours?word=WORD [&lang=en ]
Uses Polyglot's Embeddings to provide neighbouring words for 
```bash
curl http://localhost:6400/polyglot/neighbours?word=obama
```
```json
"neighbours": [
    "Bush",
    "Reagan",
    "Clinton",
    "Ahmadinejad",
    "Nixon",
    "Karzai",
    "McCain",
    "Biden",
    "Huckabee",
    "Lula"
  ]
```

### /readability - Article Extraction
Note: In most cases Newspaper performs better than Readability.

#### From URL: 
GET /readability?url=https://github.com/web64/nlpserver
```bash
curl http://localhost:6400/newspaper?url=https://github.com/web64/nlpserver
```

#### From HTML:
POST /readability [html="<html>....</html>"]
```bash
curl -d "html=<html>...</html>" http://localhost:6400/newspaper
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

## Contribute
If you are familiar with NLP or Python, please let us know how this project can be improved!

## Future tasks
- [ ] News Classification
- [ ] More sentiment anlysis options
- [ ] Translation
- [ ] List installed Spacy packages
- [ ] Add https://github.com/mozilla/readability
- [ ] Add https://github.com/Microsoft/Recognizers-Text
