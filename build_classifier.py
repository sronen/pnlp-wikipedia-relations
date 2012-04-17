import nltk
import random
import re

def parse_sent(chunk):
    words = []
    poss = []
    if 'None' in chunk:
        words.append('None')
        return words, poss
    # example:["(u'Father', 'NNP')", "(u'Thomas', 'NNP')"]
    re_paren = r"\(.*?\)"
    parts = re.findall(re_paren, chunk)
    for part in parts:
        #example: (u'Thomas', 'NNP')
        part = part[1:-1]
        word, pos = part.split('\', ')
        words.append(word[2:])
        poss.append(pos[1:-1])
    return words, poss
    
def sent_features(sent):
    # example sentence: [(u'having', 'NN')] killed [(u'Father', 'NNP'), (u'Thomas', 'NNP')]
    # capitalization
    # difference in similarity scores
    # all parts of speech
    # each word in a sentence
    re_bracket = r"\[.*?\]"
    features = {}
    subj = ''
    obj = ''
    try:
        subj, obj = re.findall(re_bracket, sent)
    except ValueError:
        print sent
    words1, pos1 = parse_sent(subj)
    
    words2, pos2 = parse_sent(obj)
    
    
    for word in words1:
        features['subject contains '+word] = word
    for word in words2:
        features['object contains '+word] = word
    features['subjpos'] = tuple(pos1)
    features['objpos'] = tuple(pos2)
    features['subjCapCount'] = len(filter(lambda x: x.istitle(), words1))
    features['objCapCount'] = len(filter(lambda x:x.istitle(), words2))

    return features

def make_featureset(filename):
    good_sents = []
    bad_sents = []
    for line in open(filename):
        try:
            sent,tag = line[:-1].split('||')
        except ValueError:
            print line
            continue
        if tag =='good':
            good_sents.append((sent,'good'))
        elif tag == 'bad':
            bad_sents.append((sent,'bad'))
    all_sents = good_sents + bad_sents
    return [(sent_features(sent), label) for (sent, label) in all_sents]

train_set = make_featureset('output_train.txt')
test_set = make_featureset('output_test.txt')
classifier = nltk.NaiveBayesClassifier.train(train_set)

