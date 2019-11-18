#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Calculate statistics on already generated random walk cporpora. 
Assumes input is a text file where 1 line = 1 sentence.


Copyright © 2019 Filip Klubička, Alfredo Maldonado. Technological University Dublin, ADAPT Centre.
All Rights Reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

__author__ = "Filip Klubička"

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-c", "--corpus", help="File name/location of the input corpus.")
    parser.add_argument("-r", "--rare", type=str, default='no', help="Lists the rare words in the corpus. Options: yes, no. Default: no")
    parser.add_argument("-u", "--unique_sentences", type=str, default='yes', help="Also calculates the number of unique sentences in the corpus and counts n-length sentences. Options: yes, no. Default: yes. NOTE: This is a bit more memory intensive, especially with larger corpora, so if you're only interested in token counts, set this to 'no'.")
    args = parser.parse_args()
    return args

args = parse_arguments()


token_count=0
types=[]
token_freq={}
rare_words=[]

sentences=[] #this stores each individual sentence as a list of tokens; needed to calculate frequency of n-word sentences 
bow_sents=[] #this stores each individual sentence as a bag of words set of tokens (i.e. not in any order and no tokens are repeated); only does this if -u argument is set to yes 


for line in open(args.corpus):
	sentences.append(line.strip().lower().split(' '))
	tokens=line.strip().lower().split(' ')

	token_count+=len(tokens) #add token count of current sentence to total token count 

	for token in tokens:
		if token not in types:
			types.append(token) #counts types (i.e. unique tokens)
		
		if len(tokens) == 1:	#we do not count 1-word sentences as occurrences of rare words, but you might wish to do so, which is what the commented code below is for
			#if token not in rare_words:
			#	rare_words.append(token)
			pass
		else:
			if token not in token_freq:
				token_freq[token]=1
			else:
				token_freq[token]+=1

	if args.unique_sentences == 'yes':
		bow_sents.append(set(line.strip().lower().split(' ')))

#Uncomment the the two lines commented below if you wish to print a list of tokens sorted by frequency
#sorted_by_value = sorted(token_freq.items(), key=lambda kv: kv[1])
#print(sorted_by_value)

#this snippet adds rare words into a printable list 
for token in token_freq:
	if token_freq[token]<10:
		if token not in rare_words:
			rare_words.append(token)

sent_count=len(sentences)

if args.rare == 'yes':
	for token in rare_words:
		print(token)
else:
	if args.unique_sentences == 'yes':

		string_sents=[]

		#turn sentence i.e. set of unique tokens into a list and sort the list alphabetically, then add that sorted list to a list of sentences
		for sent in bow_sents:
			string_sents.append(' '.join(sorted(sent)))

		#turn the *list* of alphabetically sorted sentences into a *set* of alphabetically sorted sentences, thereby removing all duplicates and obtaining a set of unique sentences  
		bagof_uniq_sents=set(string_sents)

		uniq_n=len(bagof_uniq_sents)
		same_n=sent_count-uniq_n

		print('### For a ', sent_count, ' sentence-strong corpus ###\nNumber of identical sentences: ', same_n, ' which is ', 100*(float(same_n)/(same_n+uniq_n)), 'percent of the corpus \nNumber of unique sentences: ', uniq_n, 'which is ', 100*(float(uniq_n)/(same_n+uniq_n)), 'percent of the corpus\n')

		#this snippet counts the number of sentences of length n (e.g. there's x 1-word sentences, y 2-word sentences, z 3-word sentences, etc.)
		max_sent_len=0
		for sent in sentences:
			if len(sent) > max_sent_len:
				max_sent_len=len(sent)
		sent_lens={}
		for i in range(max_sent_len+1)[1:]:
			sent_lens[i]=0
		for sent in sentences:
			if len(sent) in sent_lens:
				sent_lens[len(sent)]+=1
		for senlen in sent_lens:
			print('Number of ', senlen, '-word sentences: ', sent_lens[senlen], ' which is', 100*(float(sent_lens[senlen])/(sent_count)), 'percent of the corpus')
		
		print('\nAverage sentence length (in tokens): ', token_count/len(sentences),'\nTotal number of tokens (words) is: ', token_count, '\nNumber of types (unique words): ', len(types), '\nNumber of "rare" word types (with frequency<10):', len(rare_words), '\nPercentage of "rare" words (types):', 100*(float(len(rare_words))/(len(types))))

	else:
		print('### For a ', sent_count, ' sentence-strong corpus ###\nAverage sentence length (in tokens): ', token_count/len(sentences),'\nTotal number of tokens (words) is: ', token_count, '\nNumber of types (unique words): ', len(types), '\nNumber of "rare" word types (with frequency<10):', len(rare_words), '\nPercentage of "rare" words (types):', 100*(float(len(rare_words))/(len(types))))