#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://github.com/boudinfl/pke
import pke
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

extractor = pke.unsupervised.TopicRank()

input_text = u"""Catalonia president-elect calls on Spanish PM to talk with separatist leaders.
Quim Torra: New Catalan separatist leader sticks steadfastly to independence from Spain.
Quim Torra: Catalonia elects hardline separatist as new regional president.
Catalan Parliament Elects New Leader, a Separatist Not Under Indictment.
Catalonia votes in hardline separatist as leader.
Catalans elect new separatist leader Quim Torra.
Catalonia parliament elects Quim Torra as new regional leader.
Spanish father accused of 'evil spirits' rape.
Catalonia votes on new leader, Spain to lift direct rule.
Why HSBC whistleblower Hervé Falciani fears for his freedom.
Wins for Guerdat in Windsor & Zverev in Spain.
Torra: Catalonia looks set to vote for headline seperatist regional president.
Putting the fizz back into Catalonia's cava.
Catalonia's parliament fails to elect new president in first round of vote.
Catalan separatist Quim Torra faces presidential runoff.
Black Friday: Spanish public broadcaster employees mourn the death of independent news.
Puigdemont rejects new appointment as Catalan leader, proposes successor.
'The Germans sneeze loudly': refugees on their adopted homelands - video."""

extractor.read_text(input_text)
extractor.candidate_selection()
extractor.candidate_weighting()
keyphrases = extractor.get_n_best(n=10, stemming=False)

print("=============\n")
for phrase in keyphrases:
    print( phrase )