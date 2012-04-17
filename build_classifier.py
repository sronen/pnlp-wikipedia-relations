import nltk
import random
import re

def parse_sent(chunk):
    words = []
    poss = []
    # example:["(u'Father', 'NNP')", "(u'Thomas', 'NNP')"]
    re_paren = r"\(.*?\)"
    parts = re.findall(re_paren, chunk)
    for part in parts:
        #example: (u'Thomas', 'NNP')
        part = part.strip('()')
        word, pos = part.split(', ')
        words.append(word[2:-1])
        poss.append(pos[1:-1])
    return words, poss
    
def sent_features(sent):
    # example sentence: [(u'having', 'NN')] killed [(u'Father', 'NNP'), (u'Thomas', 'NNP')]
    # capitalization
    # difference in similarity scores
    # all parts of speech
    # each word in a sentence
    re_bracket = r"\[.*?\]"
   
    subj, obj = re.findall(re_bracket, sent)

    words1, pos1 = parse_sent(subj)
    
    words2, pos2 = parse_sent(obj)
    
    features = {}
    for word in words1+words2:
        features['contains'+word] = word
    features['subjpos'] = pos1
    features['objpos'] = pos2
    features['subjCapCount'] = len(filter(lambda x: x.istitle(), words1))
    features['objCapCount'] = len(filter(lambda x:x.istitle(), words2))
    return features

good_sents = []
bad_sents = []
for line in open('marked_examples.txt', 'r'):
    sent,tag = line.split('|')
    if tag == 'good':
        good_sents.append((sent,'good'))
    elif tag == 'bad':
        bad_sents.append((sent,'bad'))
all_sents = good_sents + bad_sents
train_set = [sent_features(sent), label) for (sent, label) in all_sents]
classifier = nltk.NaiveBayesClassifier.train(train_set)

