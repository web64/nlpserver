# NLP Server
<!-- <p align="center">
  <img src="http://cdn.web64.com/nlp-norway/nlp-server-2.png" width="400">
</p> -->

NLP Server is a Python 3 Flask web service for easy access to multilingual Natural Language Processing tasks such as language detection, article extraction, entity extraction, sentiment analysis, summarization and more.

NLP Server provides a simple API for non-python programming languages to access some of the great NLP libraries that are available in python.

The server is simple to set up and easy to integrate with your programming language of choice.

## PHP & Laravel clients
A PHP library and a Laraval package is available:
* https://github.com/web64/php-nlp-client
* https://github.com/web64/laravel-nlp


## Step1: Core Installation
The NLP Server has been tested on Ubuntu, but should work on other versions of Linux.
```bash
git clone https://github.com/web64/nlpserver.git
cd nlpserver

sudo apt-get install -y libicu-dev python3-pip
sudo apt-get install polyglot
sudo apt-get install python3-icu
pip3 install -r requirements.txt
```

### Step 2: Download Polyglot models for human languages
Polyglot is used for entity extraction, sentiment analysis and embeddings (neighbouring words).

You'll need to download the models for the languages you want to use.

```bash
# For example: English and Norwegian
python3 -m polyglot download LANG:en
python3 -m polyglot download LANG:no
```
The /status api endpoint will list installed Polyglot language modules: http://localhost:6400/status

### Step 3: Download SpaCy models for entity extraction (NER)
If you want to use the /spacy/entities endpoint for article extraction you need to download the models for the languages you want to use
```bash
# Install Spacy if not already installed
pip3 install -U spacy

# For example English, Spanish and Multi-Language
python3 -m spacy download en
python3 -m spacy download es
python3 -m spacy download xx
```


### Detailed Installation
If you have any problems installing from requirements.txt you can instead install the libraries one by one.

```bash
sudo apt-get install -y libicu-dev
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
sudo pip3 install afinn
sudo pip3 install textblob
sudo pip3 install transformer
```
The /status api endpoint will list missing python modules: http://localhost:6400/status


## Install Recipe for forge.laravel.com servers
Add this recipe on Forge and run it as root to install NLPserver as a service with Supervisor.

```bash
# Install NLPserver
cd /home/forge/
git clone https://github.com/web64/nlpserver.git
chown -R forge:forge /home/forge/nlpserver
cd /home/forge/nlpserver

# Install pkg-config. This package is used to find the ICU version
sudo apt install pkg-config

# python packages
apt-get install -y python-numpy libicu-dev
apt-get install -y python3-pip
pip3 install -r requirements.txt

# English Language models - add other models you might require
polyglot download LANG:en
python3 -m spacy download en

# Supervisor - update paths in nlpserver.conf if different
cp nlpserver.conf /etc/supervisor/conf.d
supervisorctl reread
supervisorctl update
supervisorctl start nlpserver
```

## Start NLP Server web service:
To start the server manually run:
```bash
$ nohup python3 nlpserver.py  >logs/nlpserver_out.log 2>logs/nlpserver_errors.log &
```

You can now access the web console and test that the NLP Server is working: http://localhost:6400/


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
/trans/sentiment|POST|text,lang|Sentiment analysis for provided text using transformer|polyglot
/polyglot/neighbours|GET|word,lang|Embeddings: neighbouring words|polyglot
/langid|GET,POST|text|Language detection for provided text|langid
/gensim/summarize|POST|text,word_count|Summarization of long text|gensim
/gensim/similarity|POST|text1,text2|Similarity percentage of texts|gensim
/spacy/entities|POST|text,lang|Entity extraction for provided text in given language|SpaCy

## Usage
For API responses see /response_examples/ directory.

### /newspaper - Article & Metadata Extraction
Returns article text, authors, main image, publish date and meta-data for given url or HTML.

#### From URL:
`GET /newspaper?url=http://...`
```bash
curl http://localhost:6400/newspaper?url=https://github.com/web64/nlpserver
```
Example JSON response: https://raw.githubusercontent.com/web64/nlpserver/master/response_examples/newspaper.json

#### From HTML:
`POST /newspaper [html="<html>....</html>"]`
```bash
curl -d "html=<html>...</html>" http://localhost:6400/newspaper
```

### Language Detection
`GET|POST /langid?text=what+language+is+this`

```bash
curl http://localhost:6400/langid?text=what+language+is+this
```

Returns language code of provided text
```json
langid: {
  "language": "en",
  "score": -42.31864953041077
}
```

### Polyglot Entity Extraction & Sentiment Analysis
`POST /polyglot/entities [params: text]`
```bash
curl -d "text=The quick brown fox jumps over the lazy dog" http://localhost:6400/polyglot/entities
```

### SpaCy Entity Extraction (NER)
`POST /spacy/entities [params: text, lang]`

Note: You'll need to have downloaded the language models for the language you are using.

```bash
# For example for English:
python -m spacy download en
```

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
### Sentiment Analysis
`POST /polyglot/sentiment [params: text, lang (optional)]`

```bash
curl -d "text=This is great!" http://localhost:6400/polyglot/sentiment
```
```json
{
  "message": "Sentiment Analysis API - POST only",
  "sentiment": 1.0,
}
```

###  Text summarization
`POST /gensim/summarize [params: text, word_count (optional)]`

Generates summary for long text. Size of summary by adding a word_count parameter with the maximum number of words in summary.


### Neighbouring words
`GET /polyglot/neighbours?word=WORD [&lang=en ]`

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
`GET /readability?url=https://github.com/web64/nlpserver`
```bash
curl http://localhost:6400/newspaper?url=https://github.com/web64/nlpserver
```

#### From HTML:
`POST /readability [html="<html>....</html>"]`
```bash
curl -d "html=<html>...</html>" http://localhost:6400/newspaper
```

## Run as a service:
First, install Supervisor if not already installed
```bash
sudo apt-get update && sudo apt-get install python-setuptools
sudo apt install supervisor
```
Copy `nlpserver.conf` to `/etc/supervisor/supervisord.conf` and edit paths.
Then run this to start the NLPserver:

```bash
sudo supervisorctl reread
sudo supervisroctl update
sudo supervisorctl start nlpserver
```



## Contribute
If you are familiar with NLP or Python, please let us know how this project can be improved!

## Future tasks
- [ ] News Classification
- [ ] More sentiment anlysis options
- [ ] Translation
- [ ] List installed Spacy packages
- [ ] Add https://github.com/stanfordnlp/stanfordnlp
- [ ] Add https://github.com/zalandoresearch/flair
- [ ] Add https://github.com/mozilla/readability
- [ ] Add https://github.com/Microsoft/Recognizers-Text
- [ ] Add https://github.com/alvations/pywsd
- [ ] Add https://github.com/datalib/libextract
- [ ] Add https://github.com/michaelhelmick/lassie
