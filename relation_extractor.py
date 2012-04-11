import codecs, os, re
import nltk
from chunk_wikipedia import chunk_wikitext


filename = "articles/Grass_Fight.txt"
grammar = r"""
    NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and nouns
        {<DT>?<NNP>+}                # chunk sequences of proper nouns
"""
cp = nltk.RegexpParser(grammar)
sents = nltk.sent_tokenize(open(filename).read().decode('utf-8'))
sents = map(lambda x:chunk_wikitext(x), sents)
tree = cp.parse(nltk.pos_tag(sents[0].leaves()))
tree.draw()
