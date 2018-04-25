#
#	https://github.com/web64/nlpserver
#
# To run:
# $ nohup python3 nlpserver.py  >logs/nlpserver_out.log 2>logs/nlpserver_errors.log &
#

from flask import Flask
from flask import jsonify
from flask import request
from polyglot.text import Text, Word
from newspaper import Article
import langid

app = Flask(__name__)

#  configurations
#app.config['var1'] = 'test'

default_data = {}
default_data['web64'] = {
		'app': 'nlpserver',
		'version':	'0.8',
		'last_modified': '2018-04-25',
		'link': 'http://nlpserver.web64.com/',
		'github': 'https://github.com/web64/nlp-server',
		'endpoints': ['/summarize', '/embeddings', '/language', '/polyglot', '/newspaper'],
	}

default_data['message'] = 'Welcome to NLP API by web64.com'


@app.route("/")
def main():
	data = default_data
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

	if not params['text']:
		data['error'] = '[text] parameter not found'
		return jsonify(data)

	
	# if not params['word_count']:
	# 	word_count = None
	# else:
	# 	word_count = params['word_count']
	
	#data['summary'] = summarize( text=params['text'], word_count=word_count )
	data['summary'] = summarize( text=params['text'] )

	return jsonify(data)

@app.route("/embeddings", methods=['GET'])
def embeddings():
	data = dict(default_data)
	data['message'] = "Embeddings - Find neighbors of word  API - Usage: 'word' GET parameter "
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
		data['error'] = '[lang] parameter not found'
		return jsonify(data)

	
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

@app.route("/language", methods=['GET', 'POST'])
def language():
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



@app.route("/polyglot", methods=['POST'])
def polyglot():
	data = dict(default_data)
	data['params'] = {}
	data['polyglot'] = {}

	data['params'] = request.form # postdata

	if not data['params']:
		data['error'] = 'Missing parameters'
		return jsonify(data)

	if not data['params']['text']:
		data['error'] = 'Text parameter not found'
		return jsonify(data)

	if not data['params']['lang']:
		data['params']['lang'] is None
		# data['error'] = 'lang parameter not found'
		# return jsonify(data)

	#article_content =  data['params']['text']

	polyglot_text = Text(data['params']['text'], hint_language_code=data['params']['lang'])
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




@app.route("/newspaper")
def newspaper():
	data = dict(default_data)
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
		data['params'] = request.form # postdata

		if not data['params']:
			data['error'] = 'Missing parameters'
			return jsonify(data)

		if not data['params']['html']:
			data['error'] = 'html parameter not found'
			return jsonify(data)
	
		article = Article(url='',keep_article_html=True)
		article.set_html(data['params']['html'])
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

app.run(host='0.0.0.0', port=6400)


