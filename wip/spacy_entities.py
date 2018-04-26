# -*- coding: utf-8 -*-

import spacy

nlp = spacy.load("en")

text = """
Today, Google is launching the biggest revamp of Gmail in years. The company is bringing to the flagship Gmail service many (but not all) of the features it trialed in Inbox for Gmail, and adding a few new ones, too. With those new features, which we first reported earlier this month, the company is also introducing a refreshed design for the service, though if you’ve used Gmail before, you’ll feel right at home.

If you’ve followed along with the leaks in recent weeks, none of the new features will surprise you. It’s also not a huge surprise that Google is bringing some features from Inbox over to Gmail. What did surprise me while trying out the new service ahead of today’s launch, though, is that some features that didn’t get a lot of attention in the leaks, including the new consistent sidebar with its built-in Google Calendar, Tasks and Keep integration, are maybe among the most useful of the additions here.
"""

doc = nlp( text )


entities  = {}
counters  = {}
for ent in doc.ents:
    if not ent.label_ in entities:
        entities[ent.label_] = dict()
        counters[ent.label_] = 0
    else:
        counters[ent.label_] += 1

    entities[ ent.label_ ][ counters[ent.label_] ] =  ent.text
    print(ent.text, ent.label_)

print( entities )