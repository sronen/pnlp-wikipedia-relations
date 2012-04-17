from nltk.corpus import wordnet as wn

def average_wup_similiarity(sub_tuples, obj_tuples):
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
	all_combin_values = [wn.wup_similarity(sub, obj) for sub in sub_syn for obj in obj_syn]

	# calculate average WUP similarity
	return sum(all_cobmins_values) / float(len(all_combins_values))