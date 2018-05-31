# Python2.7 Flask app for libraries not compatible with 3.6+

# Requires:
#   - nltk.download('punkt')
#   - nltk.download('averaged_perceptron_tagger')
#   - nltk.download('stopwords')
from flask import Flask, jsonify, abort, request, send_from_directory 

app = Flask(__name__)

default_data = {}
default_data['web64'] = {
		'app': 'nlpserver',
		'version':	'0.9',
		'last_modified': '2018-04-27',
		'link': 'http://nlpserver.web64.com/',
		'github': 'https://github.com/web64/nlp-server',
		'endpoints': ['/keyphrase'],
	}

default_data['message'] = 'Welcome to NLP API by web64.com'

@app.route("/")
def main():
	data = default_data
	return jsonify(data)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/keyphrase", methods=['GET', 'POST'])
def keyphrase():
    import pke
    import nltk

    extractor = pke.unsupervised.TopicRank()
    extractor.read_text(input_text)
    extractor.candidate_selection()
    extractor.candidate_weighting()
    keyphrases = extractor.get_n_best(n=10, stemming=False)

    return jsonify(data)

app.run(host='0.0.0.0', port=6400, debug=False)