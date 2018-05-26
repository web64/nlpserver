#
#	NLP Server: https://github.com/web64/nlpserver
#
#	To run:
# 	$ nohup python3 nlpserver.py  >logs/nlpserver_out.log 2>logs/nlpserver_errors.log &
#
from flask import Flask, jsonify, abort, request, send_from_directory # abort( 404 )
import os
#from polyglot.text import Text, Word

app = Flask(__name__)

#  configurations
#app.config['var1'] = 'test'

default_data = {}
default_data['web64'] = {
		'app': 'nlpserver',
		'version':	'0.9',
		'last_modified': '2018-04-27',
		'link': 'http://nlpserver.web64.com/',
		'github': 'https://github.com/web64/nlp-server',
		'endpoints': ['/summarize', '/neighbours', '/langid', '/polyglot', '/newspaper', '/readability', '/spacy/entities'],
	}

default_data['message'] = 'NLP Server by web64.com'


@app.route("/")
def main():
	data = default_data
	return jsonify(data)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/spacy/entities", methods=['GET', 'POST'])
def spacy_entities():
	import spacy
	data = dict(default_data)
	data['message'] = "Spacy.io Entities (NER) - Usage: 'text' POST parameter, 'lang' POST parameter for Spacy model (lang=en by default)"
	params = {}

	if request.method == 'GET':
		return jsonify(data)

	params = request.form # postdata

	if not params:
		data['error'] = 'Missing parameters'
		return jsonify(data)

	if not 'text' in params:
		data['error'] = '[text] parameter not found'
		return jsonify(data)

	if not 'lang' in params:
		lang = 'en'
	else:
		lang = params['lang']

	nlp = spacy.load( lang )
	doc = nlp( params['text'] )
	data['entities']  = {}
	
	counters  = {}
	for ent in doc.ents:
		if not ent.label_ in data['entities']:
			data['entities'][ent.label_] = dict()
			counters[ent.label_] = 0
		else:
			counters[ent.label_] += 1
	
		data['entities'][ ent.label_ ][ counters[ent.label_] ] =  ent.text
		#data['entities'][ent.label_].add( ent.text )

	print( data['entities'] )
	return jsonify(data)


@app.route("/summarize", methods=['GET', 'POST'])
def summarize():
	from gensim.summarization.summarizer import summarize
	data = dict(default_data)
	data['message'] = "Summarize long text - Usage: 'text' POST parameter"
	params = {}

	if request.method == 'GET':
		return jsonify(data)

	params = request.form # postdata

	if not params:
		data['error'] = 'Missing parameters'
		return jsonify(data)

	if not 'text' in params:
		data['error'] = '[text] parameter not found'
		return jsonify(data)

	if not 'word_count' in params:
		word_count = None
	else:
		word_count = params['word_count']
	
	data['summarize'] = summarize( text=params['text'], word_count=word_count )

	return jsonify(data)

@app.route("/neighbours", methods=['GET'])
def embeddings():
	from polyglot.text import Word
	data = dict(default_data)
	data['message'] = "Neighbours (Embeddings) - Find neighbors of word API - Parameters: 'word', 'lang' language (default: en)"
	params = {}
	
	params['word']= request.args.get('word')
	params['lang']= request.args.get('lang')

	if not params:
		data['error'] = 'Missing parameters'
		return jsonify(data)

	if not params['word']:
		data['error'] = '[word] parameter not found'
		return jsonify(data)

	if not params['lang']:
		# data['error'] = '[lang] parameter not found'
		# return jsonify(data)
		params['lang'] = 'en'

	data['neighbours'] = {}

	try:
		word = Word(params['word'], language=params['lang'])
	except KeyError:
		data['error'] = 'ERROR: word not found'
		return jsonify(data)

	if not word:
		data['error'] = 'word not found'
		return jsonify(data)

	data['neighbours'] = word.neighbors

	return jsonify(data)

@app.route("/langid", methods=['GET', 'POST'])
def language():
	import langid
	data = dict(default_data)
	data['message'] = "Language Detection API - Usage: 'text' GET/POST parameter "
	data['langid'] = {}
	params = {}
	

	if request.method == 'GET':
		params['text'] = request.args.get('text')
	elif request.method == 'POST':
		params = request.form # postdata
	else:
		data['error'] = 'Invalid request method'
		return jsonify(data)

	if not params:
		data['error'] = 'Missing parameters'
		return jsonify(data)

	if not params['text']:
		data['error'] = '[text] parameter not found'
		return jsonify(data)

	lang_data = langid.classify( params['text'] ) 
	data['langid']['language'] = lang_data[0]
	data['langid']['score'] = lang_data[1]

	data['message'] = "Detected Language: " + data['langid']['language']

	return jsonify(data)



@app.route("/polyglot", methods=['GET','POST'])
def polyglot():
	from polyglot.text import Text

	data = dict(default_data)
	data['message'] = "Entity Extraction and Sentiment Analysis API- POST only"
	data['params'] = {}
	data['polyglot'] = {}

	data['params'] = request.form # postdata

	if not data['params']:
		data['error'] = 'Missing parameters'
		return jsonify(data)

	if not data['params']['text']:
		data['error'] = 'Text parameter not found'
		return jsonify(data)

	if not 'lang' in data['params']:
		language = 'en' # default language
	else:
		language = data['params']['lang']
	
	return jsonify(data)

	polyglot_text = Text(data['params']['text'], hint_language_code=language)
	data['polyglot']['entities'] = polyglot_text.entities
	data['polyglot']['sentiment'] = polyglot_text.polarity
	# if len(data['params']['text']) > 100:
	# 	data['polyglot']['sentiment'] = polyglot_text.polarity
	# else:
	# 	data['polyglot']['sentiment'] = 0


	

	data['polyglot']['type_entities']  = {}
	if polyglot_text.entities:
		counter = 0
		for entity in polyglot_text.entities:
			data['polyglot']['type_entities'][counter] = {}
			data['polyglot']['type_entities'][counter][entity.tag] = {}
			data['polyglot']['type_entities'][counter][entity.tag] = entity
			counter += 1

	return jsonify(data)


# https://github.com/buriy/python-readability
@app.route("/readability", methods=['GET', 'POST'])
def readability():
	import requests
	from readability import Document	
	from bs4 import BeautifulSoup 

	data = dict(default_data)
	data['message'] = "Article Extraction by Readability"
	data['params'] = {}
	data['error'] = ''
	data['readability'] = {}

	if request.method == 'GET':
		data['params']['url'] = request.args.get('url')
		if not data['params']['url']:
			data['error'] = '[url] parameter not found'
			return jsonify(data)

		response = requests.get( data['params']['url'] )
		doc = Document(response.text)

	elif request.method == 'POST':
		params = request.form # postdata

		if not params:
			data['error'] = 'Missing parameters'
			return jsonify(data)

		if not params['html']:
			data['error'] = 'html parameter not found'
			return jsonify(data)
	
		doc = Document( params['html'] )
	
	data['readability']['title'] = doc.title()
	data['readability']['short_title'] = doc.short_title()
	#data['readability']['content'] = doc.content()
	data['readability']['article_html'] = doc.summary( html_partial=True )

	soup = BeautifulSoup(data['readability']['summary']) 
	data['readability']['text'] =  soup.get_text() 

	return jsonify(data)

@app.route("/newspaper", methods=['GET', 'POST'])
def newspaper():
	from newspaper import Article
	import langid

	data = dict(default_data)
	data['message'] = "Article Extraction by Newspaper, and Language Detection by Langid"
	data['params'] = {}
	data['error'] = ''
	data['newspaper'] = {}
	data['langid'] = {}

	if request.method == 'GET':
		data['params']['url'] = request.args.get('url')
		if not data['params']['url']:
			data['error'] = '[url] parameter not found'
			return jsonify(data)

		article = Article(url=data['params']['url'],keep_article_html=True)
		article.download()
	elif request.method == 'POST':
		params = request.form # postdata

		if not params:
			data['error'] = 'Missing parameters'
			return jsonify(data)

		if not params['html']:
			data['error'] = 'html parameter not found'
			return jsonify(data)
	
		article = Article(url='',keep_article_html=True)
		article.set_html( params['html'] )
	else:
		data['error'] = 'Invalid request method'
		return jsonify(data)
	
	
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

	return jsonify(data)

app.run(host='0.0.0.0', port=6400, debug=False)


