import requests
from readability import Document
from pprint import pprint

response = requests.get('https://laravel-news.com/announcing-building-a-chatbot-with-laravel-and-botman')

doc = Document(response.text)
# API methods:
# .title() -- full title
# .short_title() -- cleaned up title
# .content() -- full content
# .summary() -- cleaned up content
data = dict()
data['title'] = doc.title()
data['short_title'] = doc.short_title()
data['content'] = doc.content()
data['summary'] = doc.summary()


pprint( data )
