import pke

# initialize TopicRank and set the language to French (used during candidate
# selection for filtering stopwords)
extractor = pke.unsupervised.TopicRank('norwegian_processed.txt', language='norwegian')

# load the content of the document and perform French stemming (instead of
# Porter stemmer)
extractor.read_document(format='preprocessed', stemmer='norwegian')

# keyphrase candidate selection, here sequences of nouns and adjectives
# defined by the French POS tags NPP, NC and ADJ
extractor.candidate_selection(pos=["NPP", "NC", "ADJ"])

# candidate weighting, here using a random walk algorithm
extractor.candidate_weighting()

# N-best selection, keyphrases contains the 10 highest scored candidates as
# (keyphrase, score) tuples
keyphrases = extractor.get_n_best(n=10)
print("=============\n")
for phrase in keyphrases:
    print( phrase )