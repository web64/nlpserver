#
#	NLP Server: https://github.com/web64/nlpserver
#
#	To run:
# 	$ nohup
#	It is recommended to combine FastAPI Uvicorn server with a process manager like Gunicorn and set ip up behind Nginx

from tkinter import E
import uvicorn
from typing import Optional
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import FastAPI, Request, Form
from fastapi.exceptions import HTTPException
import json
import os
from pathlib import Path
from loguru import logger
import spacy
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from datetime import datetime
import spacy
# We need to download spacy's models a priori
import subprocess
import sys
from fastapi.encoders import jsonable_encoder
from polyglot.text import Word
from gensim.summarization.summarizer import summarize
import langid
from polyglot.text import Text
from readability import Document	
from bs4 import BeautifulSoup 
from afinn import Afinn
from newspaper import Article

def install(lang, model):
	subprocess.check_call([sys.executable, "-m", "spacy", "download", model])
	subprocess.check_call([sys.executable, "-m", "polyglot", "download", "sentiment2.{}".format(lang)])
	subprocess.check_call([sys.executable, "-m", "polyglot", "download", "embeddings2.{}".format(lang)])
	subprocess.check_call([sys.executable, "-m", "polyglot", "download", "ner2.{}".format(lang)])

logger.remove()
logger.add('logs/{time}.log', rotation='00:00',
		   format="{time:HH:mm:ss} | {level} | <level>{message}</level>")

app = FastAPI()

default_data = {}
default_data['web64'] = {
		'app': 'nlpserver',
		'version':	'2.0.0',
		'last_modified': '2022-05-10',
		'documentation': 'http://nlpserver.web64.com/',
		'github': 'https://github.com/web64/nlp-server',
		'endpoints': ['/status', '/gensim/summarize', '/polyglot/neighbours', '/langid', '/polyglot/entities',
					 '/polyglot/sentiment', '/newspaper', '/readability', '/spacy/entities', '/afinn'],
	}

default_data['message'] = 'NLP Server by web64.com'
data = default_data

templates = Jinja2Templates(directory="templates")

config_data = {}

# Externalize to config file
language_models = {
   'no': 'nb_core_news_lg',
   'nl': 'nl_core_news_sm',
   'en': 'en_core_web_md'
}

for lang, model in language_models.items():
   install(lang, model)


def load_models(language_models):
	loaded_models = {model: spacy.load(model)
									   for lang, model in language_models.items()}

	default_data = {'web64':
					{
						'app': 'fastapi-spacy-ner',
						'version':	'0.0.1',
						'last_modified': '{}'.format(datetime.now()),
						'documentation': 'http://nlpserver.web64.com/',
						'github': 'https://github.com/web64/spacy-ner-server',
						'endpoints': ['/spacy/entities'],
						'available_models': language_models
					}
				}

	config_data["default_data"] = default_data
	config_data["ner_models"] = loaded_models
	logger.debug("Application config data:\n {}".format(config_data))

	return None


load_models(language_models)


@app.route("/")
async def main(request: Request):
	return templates.TemplateResponse("form.html", {"request": request})


@app.get('/favicon.ico')
async def favicon(request: Request):
	return FileResponse('static/favicon.ico')


@app.post("/spacy/entities")
async def predict(text: str = Form(...), lang=Form(...)):
	"""
	Args (from Form):
		lang: str containing the language model to query (maps to a model)
		text: str containing the text to be processed
	Returns:
		prediction: JSON object containing the entities detected in the input text
	"""

	if not lang:
		data['error'] = '[lang] no language specified'
		return jsonable_encoder(data)

	if lang:
		if lang in list(language_models.keys()):
			model_to_load = language_models[lang]
			ner_model = config_data['ner_models'][model_to_load]
		else:
			data['error'] = '[lang] invalid language specified'
			return jsonable_encoder(data)

	doc = ner_model(text)

	data['entities'] = {}
	data['message'] = "Spacy.io Named Entity Recognition (NER)"

	counters = {}
	for ent in doc.ents:
		if ent.label_ not in data['entities']:
			data['entities'][ent.label_] = {}
			counters[ent.label_] = 0
		else:
			counters[ent.label_] += 1

		data['entities'][ent.label_][counters[ent.label_]] = ent.text

	return jsonable_encoder(data)


@app.post("/gensim/summarize")
async def gensim_summarize(text: str = Form(...), word_count: int = Form(...)):
	"""
	Args (from Form):
		text: str containing the text to be processed
	Returns:
		prediction: JSON object containing the summarized input text
	"""

	data['message'] = "Summarize long text by gensim"

	if not text:
		data['error'] = '[text] parameter not found'
		return jsonable_encoder(data)

	data['summarize'] = summarize(text=text, word_count=word_count)

	return jsonable_encoder(data)


@app.post("/polyglot/neighbours")
async def embeddings(word: str = Form(...), lang=Form(...)):
	"""
	Args (from Form):
		word: str word to get neighbours from
		lang: str language to consider
	Returns:
		prediction: JSON object containing the neighbouring words for the input word
	"""

	if not word:
		data['error'] = '[word] parameter not found'
		return jsonable_encoder(data)

	if not lang:
		lang = 'en'

	data['neighbours'] = {}
	data['message'] = "Neighbours (Embeddings) - Find neighbors of word by Polyglot"

	try:
		word = Word(word, language=lang)
	except KeyError:
		data['error'] = 'ERROR: word not found'
		return jsonable_encoder(data)

	if not word:
		data['error'] = 'word not found'
		return jsonable_encoder(data)

	data['neighbours'] = word.neighbors

	return jsonable_encoder(data)


@app.post("/langid")
def language(text: str = Form(...)):
	"""
	Args (from Form):
		text: str text to identify the language
	Returns:
		prediction: JSON object containing the detected language
	"""

	data['langid'] = {}
	data['message'] = "Language Detection by Polyglot"

	lang_data = langid.classify(text) 
	data['langid']['language'] = lang_data[0]
	data['langid']['score'] = lang_data[1]

	data['message'] = "Detected Language: " + data['langid']['language']

	return jsonable_encoder(data)


@app.post("/polyglot/sentiment")
def polyglot_sentiment(text: str = Form(...), lang=Form(...)):
	"""
	Args (from Form):
		text: str text to identify the sentiment\polarity
		lang: language of the input text
	Returns:
		prediction: JSON object containing the detected sentiment
	"""

	data['sentiment'] = {}
	data['message'] = "Sentiment Analysis by Polyglot"

	if not lang:
		lang = 'en' # default language
	
	polyglot_text = Text(text, hint_language_code=lang)
	data['sentiment'] = polyglot_text.polarity

	return jsonable_encoder(data)


@app.post("/polyglot/entities")
def polyglot_entities(text: str = Form(...), lang: str = Form(...)):
	"""
	Args (from Form):
		text: str text to extract entities from
		lang: language of the input text
	Returns:
		prediction: JSON object containing the extracted entities
	"""

	data['polyglot'] = {}
	data['message'] = "Entity Extraction and Sentiment Analysis by Polyglot"

	if not text:
		data['error'] = 'Text parameter not found'
		return jsonable_encoder(data)

	if not lang:
		language = 'en' # default language
	else:
		language = lang
	
	
	polyglot_text = Text(text, hint_language_code=language)

	data['polyglot']['entities'] = polyglot_text.entities
	
	try:
		data['polyglot']['sentiment'] = polyglot_text.polarity
	except:
		data['polyglot']['sentiment'] = 0
	if len(text) > 100:
		data['polyglot']['sentiment'] = polyglot_text.polarity
	else:
	 	data['polyglot']['sentiment'] = 0

	data['polyglot']['type_entities']  = {}
	if polyglot_text.entities:
		counter = 0
		for entity in polyglot_text.entities:
			data['polyglot']['type_entities'][counter] = {}
			data['polyglot']['type_entities'][counter][entity.tag] = {}
			data['polyglot']['type_entities'][counter][entity.tag] = entity
			counter += 1

	return jsonable_encoder(data)


# https://github.com/buriy/python-readability
@app.post("/readability")
def readability(html: str = Form(...)):
	"""
	Args (from Form):
		html: str html text to extract clean text from
	Returns:
		prediction: JSON object containing the cleaned text
	"""

	data['readability'] = {}
	data['message'] = "Article Extraction by Readability"

	doc = Document(html)
	
	data['readability']['title'] = doc.title()
	data['readability']['short_title'] = doc.short_title()
	#data['readability']['content'] = doc.content()
	data['readability']['article_html'] = doc.summary(html_partial=True)

	soup = BeautifulSoup(data['readability']['article_html']) 
	data['readability']['text'] =  soup.get_text() 

	return jsonable_encoder(data)


@app.route("/afinn")
def afinn_sentiment(text: str = Form(...), lang: str = Form(...)):
	"""
	Args (from Form):
		text: str text to identify the sentiment\polarity
		lang: str language of the input text
	Returns:
		prediction: JSON object containing the detected sentiment
	"""

	data['afinn'] = 0
	data['message'] = "Sentiment Analysis by afinn"

	if not lang:
		language = 'en' # default language
	else:
		language = lang

	afinn = Afinn( language=language )
	data['afinn'] = afinn.score(text)

	return jsonable_encoder(data)


@app.post("/newspaper")
@app.get("/newspaper")
def newspaper(request: Request, url: Optional[str] = None, html: Optional[str] = None):
	"""
	Args (from Form):
		text: str url to extract the article from
		lang: str html to extract the article from
	Returns:
		prediction: JSON object containing the detected sentiment
	"""

	data['message'] = "Article Extraction by Newspaper, and Language Detection by Langid"
	data['newspaper'] = {}
	data['langid'] = {}

	if request.method == 'GET':
		if not url:
			data['error'] = '[url] parameter not found'
			return jsonable_encoder(data)

		article = Article(url=url,keep_article_html=True)
		article.download()

	elif request.method == 'POST':
		if not html:
			data['error'] = 'html parameter not found'
			return jsonable_encoder(data)
	
		article = Article(url='',keep_article_html=True)
		article.set_html(html)
	
	# Parse html 
	article.parse()

	data['newspaper']['article_html'] = article.article_html
	data['newspaper']['text'] = article.text
	data['newspaper']['title'] = article.title
	data['newspaper']['authors'] = article.authors
	data['newspaper']['top_image'] = article.top_image
	data['newspaper']['canonical_url'] = article.canonical_link
	data['newspaper']['meta_data'] = article.meta_data

	data['newspaper']['meta_description'] = article.meta_description
	if article.publish_date:
		data['newspaper']['publish_date'] = '{0:%Y-%m-%d %H:%M:%S}'.format(article.publish_date)

	data['newspaper']['source_url'] = article.source_url
	data['newspaper']['meta_lang'] = article.meta_lang

	#Detect language
	if len(article.text)  > 100:
		lang_data = langid.classify( article.title + ' ' + article.text ) 
		data['langid']['language'] = lang_data[0]
		data['langid']['score'] = lang_data[1]

	return jsonable_encoder(data)