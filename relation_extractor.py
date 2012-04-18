import codecs, os, re
import nltk
import random
from chunk_wikipedia import chunk_wikitext

def print_context(lst, index, span=2):
    print lst[index-span:index+span]
    
def return_indices(lst, verbs):
    indices = []
    for verb in verbs:
        i = -1
        while True:
            try:
                i = lst.index(verb, i+1)
            except ValueError:
                break
            indices.append(i)
    return indices

def find_np(tree, reverse=False):
    if reverse:
        itr = reversed(tree)
    else:
        itr = iter(tree)
    for tnode in itr:
        try:
            tnode.node
        except AttributeError:
            pass
        else:
            if tnode.node == 'NP':
                return tnode.leaves()
    return None
        

def run_parser(filename):
    verbs = ["killed", "murdered", "assassinated", "slaughtered"]
    grammar = r"""
               NP: {<DT|PRP\$>?<CD>*<JJ.*>*<NN|NN.*>+} # chunk determiner/possessive, adjectives and nouns
               """
    cp = nltk.RegexpParser(grammar)
    sents = []
    try:
        sents = nltk.sent_tokenize(open(filename).read().decode('utf-8'))
    except:
        print filename

    sents =  map(lambda x:chunk_wikitext(x), sents)
    good_sents = [sent for sent in sents for verb in verbs if verb in sent]
    good_sents_pos = map(lambda x:nltk.pos_tag(x.leaves()), good_sents)
    #print good_sents_pos
    count = 0
    for gsp in good_sents_pos:
        indices = return_indices([t[0] for t in gsp], verbs)
        for i in indices:
            if gsp[i][1] == 'VBD':
                left = gsp[:i]
                right = gsp[i+1:]
                lefttree = cp.parse(left)
                righttree = cp.parse(right)
                leftnp = find_np(lefttree, True)
                rightnp = find_np(righttree)
                print leftnp, gsp[i][0], rightnp
                count += 1
    return count

if __name__ == "__main__":
    path = 'articles'
    count = 0
    dirlist = os.listdir(path)
    random.shuffle(dirlist)
    for filename in dirlist:
        fullname = path+'/'+filename
        #print '***** '+ filename
        count += run_parser(fullname)
        if count >= 100:
            exit()

#if len(good_sents) == 0:
#    print "no match"
#else:
    #tree = cp.parse(nltk.pos_tag(good_sents[0].leaves()))
    #tree.draw()
