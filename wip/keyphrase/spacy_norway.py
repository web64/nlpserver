import spacy

nb = spacy.load("nb_dep_ud_sm")

with open('norwegian.txt', 'r') as myfile:
    text=myfile.read().replace('\n', ' ')

doc = nb(text)

processed_text = '';

for token in doc:
    #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
    processed_text += token.text +"/" + token.pos_ + " "

print(processed_text)

with open("norwegian_processed.txt", 'a') as out:
    out.write(processed_text + '\n')

