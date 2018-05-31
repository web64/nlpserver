import pke

# initialize TopicRank and set the language to French (used during candidate
# selection for filtering stopwords)
extractor = pke.unsupervised.TopicRank(input_file='french.txt', language='french')
print("pke.unsupervised.TopicRank")
print(extractor)

# load the content of the document and perform French stemming (instead of
# Porter stemmer)
extractor.read_document(format='preprocessed', stemmer='french')
print("extractor.read_document")
print(extractor)

# keyphrase candidate selection, here sequences of nouns and adjectives
# defined by the French POS tags NPP, NC and ADJ
extractor.candidate_selection(pos=["NPP", "NC", "ADJ"])
print("extractor.candidate_selection")
print(extractor)

# candidate weighting, here using a random walk algorithm
extractor.candidate_weighting()
print(extractor)

# N-best selection, keyphrases contains the 10 highest scored candidates as
# (keyphrase, score) tuples
keyphrases = extractor.get_n_best(n=10)
print(keyphrases)