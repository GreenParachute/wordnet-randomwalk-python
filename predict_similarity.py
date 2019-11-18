#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Predicts word similarity for given word representations.
Requires trained embeddings as input and a file with a list of word pairs.


Copyright © 2019 Filip Klubička, Alfredo Maldonado. Technological University Dublin, ADAPT Centre.
All Rights Reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""

import pickle
import argparse
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

__author__ = "Alfredo Maldonado"


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--word2idx1', type=str)
    parser.add_argument('--word2idx2', type=str)
    parser.add_argument('--vecs1', type=str)
    parser.add_argument('--vecs2', type=str)
    parser.add_argument('--smwe', action='store_true', help="Sum multi-word expressions")
    parser.add_argument('--default', action='store_true', help="Use mean of matrix as default value if word is not found")
    parser.add_argument('--test', type=str)
    parser.add_argument('--out', type=str)
    args = parser.parse_args()
    return args


def main(args):
    word2idx1 = pickle.load(open(args.word2idx1, 'rb')) if args.vecs1.endswith(".dat") else None  # assume faruqui-retrofit vectors
    word2idx2 = pickle.load(open(args.word2idx2, 'rb')) if args.word2idx2 is not None else None
    predict(args.test, args.out, word2idx1, args.vecs1, word2idx2, args.vecs2, args.smwe, args.default)


def predict(test, out, word2idx1, vecs1, word2idx2=None, vecs2=None, sum_mwes=False, default=False):
    idx2vec1 = None
    if word2idx1 is not None:
        try:
            idx2vec1 = pickle.load(open(vecs1, 'rb'))
        except UnicodeDecodeError:  # assume it's a polyglot pretrained embedding
            with open(vecs1, 'rb') as f:
                u = pickle._Unpickler(f)
                u.encoding = 'latin1'
                p = u.load()
                pass  
    else:  # assume it's from faruqui-retrofit
       word2idx1, idx2vec1 = read_from_retrofit(vecs1)
    idx2vec2 = pickle.load(open(vecs2, 'rb')) if vecs2 is not None else None
    def_vec1 = idx2vec1.mean(axis=0) if default else None
    def_vec2 = idx2vec2.mean(axis=0) if default and word2idx2 is not None else None
    with open(test, 'r', encoding='utf-8') as f_in, open(out, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            line = line.strip().lower()
            word_pair = line.split("\t")
            wv1 = get_vector(word_pair[0], word2idx1, idx2vec1, word2idx2, idx2vec2, sum_mwes, def_vec1, def_vec2)
            wv2 = get_vector(word_pair[1], word2idx1, idx2vec1, word2idx2, idx2vec2, sum_mwes)
            score = cosine_similarity(wv1.reshape(1, -1), wv2.reshape(1, -1))[0][0]
            f_out.write("{}\n".format(score))


def get_vector(word, word2idx1, idx2vec1, word2idx2=None, idx2vec2=None, sum_mwes=False, vec1_default=None, vec2_default=None):
    wvec = np.zeros(idx2vec1.shape[1] + (idx2vec2.shape[1] if idx2vec2 is not None else 0))
    for unigram in word.split(' ') if sum_mwes else [word]:
        unigram_id1 = word2idx1.get(unigram, None)
        unigram_id2 = word2idx2.get(unigram, None) if word2idx2 is not None else None
        if unigram_id1 is not None:
            wvec += np.concatenate((idx2vec1[unigram_id1], np.zeros(idx2vec2.shape[1])), axis=0) if idx2vec2 is not None else idx2vec1[unigram_id1]
        elif vec1_default is not None:
            wvec += np.concatenate((vec1_default, np.zeros(idx2vec2.shape[1])), axis=0) if idx2vec2 is not None else vec1_default
        if idx2vec2 is not None:
            if unigram_id2 is not None:
                wvec += np.concatenate((np.zeros(idx2vec1.shape[1]), idx2vec2[unigram_id2]), axis=0)
            elif vec2_default is not None:
                wvec += np.concatenate((np.zeros(idx2vec1.shape[1]), vec2_default), axis=0)
    return wvec


def read_from_retrofit(vec_file):
    word2idx = {}
    idx2vec = []
    idx = 0
    with open(vec_file, 'r') as f:
        for line in f:
            values = line.strip().split()
            word = values[0]
            vector = [float(value) for value in values[1:]]
            word2idx[word] = idx
            idx2vec.append(vector)
            idx += 1
    return word2idx, np.array(idx2vec)


if __name__ == "__main__":
    main(args=parse_args())
