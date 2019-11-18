#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Produces a synthetic corpus based on a random walk of nltk's WordNet

"""

__author__ = "Filip Klubička and Alfredo Maldonado"

from nltk.corpus import wordnet as wn
import random
import numpy as np
import pandas as pd
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-a", "--alpha", type=float, default=0.85, help="Probability to continue producing a sentence. Default: 0.85")
    parser.add_argument("-s", "--size", type=int, default=1000, help="Size of corpus to produce (in terms of --unit). Default: 1000")
    parser.add_argument("-u", "--unit", type=str, default='line', help="Unit to use for --size. Options: line, token. Default: line")
    parser.add_argument("-o", "--output", help="Output corpus file name/location")
    parser.add_argument("-m", "--min", type=int, default='1', help="Minimum sentence length. Default: 1")
    parser.add_argument("-d", "--direction", type=str, default='both', help="Hierarchy direction constraint on the random walk. Options: up, down, both. Default: both)")
    parser.add_argument("-i", "--mwe", type=str, default='no', help="Do you wish to split multi-word expressions (MWEs) into words with spaces? Options: yes, no. Default: no")
    args = parser.parse_args()
    return args

#function that chooses a lemma from a synset based on lemma frequency count, which is in turn interpreted as its probability
def choose_lemma(lemmas):
    lemma_freq = []
    for lemma in lemmas:
        freq = lemma.count()
        if freq == 0:  # this is so that there is always at least 1 occurence of all words we have
            lemma_freq.append(1)
        else:
            lemma_freq.append(freq)
    total = sum(lemma_freq)

    probs = []
    for freq in lemma_freq:
        probs.append(float(freq) / total)
    index = np.random.choice(np.arange(0, len(probs)), p=probs)
    lemma = lemmas[index]

    return lemma

args = parse_arguments()

corpus_size = args.size
counter = 0
alpha = args.alpha  # by default, the probability to terminate is 0.15 and the probability to go on is 0.85
terminate = 0
i = 1000

all_synsets = list(wn.all_synsets())
synset = random.choice(all_synsets) #this chooses a random synset from set of all synsets and so initialises the random walk

visited_synsets = {synset : {'init' : 1, 'walk' : 0} } #this keeps track of how many times a synset has been visited 
sent_lens = 0 #total sum of the lengths of all generated sentences in number of words (tokens)

with open(args.output, 'w') as f:
    while (counter < corpus_size):
        sentence = []
        while np.random.choice(np.arange(0, 2), p=[alpha, 1 - alpha]) != 1:
            lemmas = synset.lemmas()

            lemma = choose_lemma(lemmas) 
            #lemma = random.choice(lemmas) #if you'd rather just choose a random lemma 
            
            if lemma not in sentence:
                sentence.append(lemma)
            else:
                continue

            #ensures the random walk takes the desired direction
            if args.direction == 'both':
                edges = synset.hypernyms() + synset.hyponyms()
            elif args.direction == 'up':
                edges = synset.hypernyms()
            elif args.direction == 'down':
                edges = synset.hyponyms()
            
            #increases counter for the visited synset
            if len(edges) != 0:
                synset = random.choice(edges)
                if synset in visited_synsets:
                    visited_synsets[synset]['walk'] = visited_synsets[synset].get('walk', 0) + 1
                else:
                    visited_synsets[synset] = {'walk' : 1, 'init' : 0}
            else:
                break
        
        #if statement ensures that the desired number and length of sentences are generated
        if len(sentence) > args.min-1:
            sentence_str = ""
            if args.mwe == 'yes':
                for lemma in sentence:
                    sentence_str += ' '.join(lemma.name().split('_')) + ' '  #treats multi-word expressions (MWEs) as words with spaces
            elif args.mwe == 'no':
                for lemma in sentence:
                    sentence_str += lemma.name() + ' '  #treats multi-word expressions (MWEs) as separate lemmas, with underscore
            sentence_str = sentence_str.replace("'s", " 's")
            f.write(sentence_str.rstrip() + '\n') #writes output sentence into the corpus file
            sent_lens += len(sentence_str.split()) #increases total token count
            
            if args.unit == 'token':
                counter += len(sentence_str.split())
                if counter % 1000 == 0:
                    print('Generated',i, 'tokens...')
                    i+=1000
            else:  # defaults to 'line'
                counter += 1
                if counter % 1000 == 0:
                    print('Generated',i, 'sentences...')
                    i+=1000                
        
        #pick a new random synset and thus initialise a new random walk
        synset = random.choice(all_synsets)
        if synset in visited_synsets:
            visited_synsets[synset]['init'] = visited_synsets[synset].get('init', 0) + 1
        else:
            visited_synsets[synset] = {'init' : 1, 'walk' : 0}
        sentence = [] #clear sentence before new loop begins


print("\nVisited: " + str(len(visited_synsets)) + " out of " + str(len(all_synsets)) + " synsets, i.e. " +
      str(100 * len(visited_synsets) / float(len(all_synsets))) + " percent of WordNet.\nAverage sentence length is: " +
      str(sent_lens / float(corpus_size)) + " lemmas.")
print("Number of nodes visited:")
#this is to break down the total visits into visits of nodes walked to and nodes visited by random initialization
walkfreq = {}
initfreq = {}
freqfreq = {}
for synset in visited_synsets:
    walk = int(visited_synsets[synset]['walk'])
    init = int(visited_synsets[synset]['init'])
    freq = int(visited_synsets[synset]['init']+visited_synsets[synset]['walk'])
    walkfreq[walk] = walkfreq.get(walk, 0) + 1
    initfreq[init] = initfreq.get(init, 0) + 1
    freqfreq[freq] = freqfreq.get(freq, 0) + 1

#the following code uses pandas to tidy up the output statistics
d = {'total_nodes':[],'total_visits':[],'init_nodes':[],'init_visits':[],'walk_nodes':[],'walk_visits':[]}

for freq in sorted(freqfreq):
    d['total_nodes'].append(freqfreq[freq])
    d['total_visits'].append(freq)
d['total_nodes']=pd.Series(d['total_nodes'])
d['total_visits']=pd.Series(d['total_visits'])
for init in sorted(initfreq):
    d['init_nodes'].append(initfreq[init])
    d['init_visits'].append(init)
d['init_nodes']=pd.Series(d['init_nodes'])
d['init_visits']=pd.Series(d['init_visits'])
for walk in sorted(walkfreq):
    d['walk_nodes'].append(walkfreq[walk])
    d['walk_visits'].append(walk)
d['walk_nodes']=pd.Series(d['walk_nodes'])
d['walk_visits']=pd.Series(d['walk_visits'])

df = pd.DataFrame(d, dtype=object)
df = df[['total_nodes','total_visits','init_nodes','init_visits','walk_nodes','walk_visits']]
pd.set_option('display.expand_frame_repr', False)
with pd.option_context('display.max_rows', None, 'display.max_columns', 7):
    print(df)