import nltk
import random
import re
#from avg_wup_similarity import average_wup_similarity
from nltk.corpus import wordnet as wn

def parse_sent(chunk):
    words = []
    poss = []
    tuples = []
    if 'None' in chunk:
        words.append('None')
        return words, poss, tuples, True
    # example:["(u'Father', 'NNP')", "(u'Thomas', 'NNP')"]
    re_paren = r"\(.*?\)"
    parts = re.findall(re_paren, chunk)
    for part in parts:
        #example: (u'Thomas', 'NNP')
        part = part[1:-1]
        word, pos = part.split('\', ')
        word = word[2:]
        pos = pos[1:-1]
        words.append(word)
        poss.append(pos)
        tuples.append((word, pos))
    return words, poss, tuples, False
    
def average_wup_similarity(sub_tuples, obj_tuples):
	'''
	Get a list of subject tuples and a list of object tuples, and calculate
	the average wup_similarity for all combinations between them
	
	Example formats:
	sub_words = [('three', 'CD'), ('percent', 'NN')]

	obj_words = [(').', 'NNP'), ('==', 'NNP'), ('Northern', 'NNP'), ('Virginia', 'NNP'), ('Campaign', 'NNP'), ('==', 'NNP'), ('The', 'NNP'), ('Coast', 'NNP'), ('Division', 'NNP')]
	
	'''
	# get WordNet SynSets for all nouns
	sub_syn = [wn.synsets(word)[0] for (word, det) in sub_tuples if det.startswith('NN') and len(wn.synsets(word))>0]
	obj_syn = [wn.synsets(word)[0] for (word, det) in obj_tuples if det.startswith('NN') and len(wn.synsets(word))>0]

	# get all subject-object combinations
	all_combins_values = [wn.wup_similarity(sub, obj) for sub in sub_syn for obj in obj_syn]
        # filter out all the None values
        all_combins_values = filter(lambda x: x is not None, all_combins_values)
        # it's possible that obj_syn or sub_syn doesnt have a value because some words dont have synsets
        if len(all_combins_values) == 0:
            return 0.0
	# calculate average WUP similarity
	return sum(all_combins_values) / float(len(all_combins_values))

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
    words1, pos1, tuples1, isNone1 = parse_sent(subj)
    
    words2, pos2, tuples2, isNone2 = parse_sent(obj)
    
    
    for word in words1:
        features['subject contains '+word] = word
    for word in words2:
        features['object contains '+word] = word
    features['subjpos'] = tuple(pos1)
    features['objpos'] = tuple(pos2)
    features['subjCapCount'] = len(filter(lambda x: x.istitle(), words1))
    features['objCapCount'] = len(filter(lambda x:x.istitle(), words2))
    features['wupSimilarity'] = 0 if isNone1 is True or isNone2 is True else average_wup_similarity(tuples1, tuples2)
    features['wupBin'] = 0 if features['wupSimilarity'] < 0.5 else 1
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

