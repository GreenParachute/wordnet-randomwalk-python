
# WordNet Random Walk in Python 

## Using and understanding the provided scripts


### Generate a random walk corpus:

Run `wn_random_walk.py` to generate the pseudo corpus of a given size and constraints from the WordNet taxonomy.

The possible options and corresponding arguments are:

* -s, --size : Size of corpus to produce (in terms of --unit). Default: 1000.
* -u, --unit : Unit to use for --size. Options: line, token. Default: line.
* -d, --direction : Hierarchy direction constraint on the random walk. Options: up, down, both. Default: both.
* -m, --min : Minimum sentence length. Default: 1.
* -i, --mwe : Split multi-word expressions (MWEs) into words with spaces. Options: yes, no. Default: no.
* -a, --alpha : Probability to continue producing a sentence. Default: 0.85.
* -o, --output : Output corpus file name/location.
   
Example command:

`python wn_walk.py --size 1000 --unit token --direction down --min 2 --mwe yes --alpha 0.9 --output wn-corpus.1k.up.2ws.txt`

You can download the various taxonomic random walk corpora that we generated for our work [here](https://arrow.dit.ie/datas/9/).


### Calculate basic corpus statistics:

Run `corpus_statistics.py` to calculate statistics such as: total token count, total type count, rare word type count, percentage of rare words in the vocabulary, average sentence length, number of unique sentences and number of sentences of length n (n<=10).

The possible options and corresponding arguments are:

* -c, --corpus : File name/location of the input corpus.
* -r, --rare : Prints a list of the rare words in the corpus. Options: yes, no. Default: no.
* -u, --unique_sentences : Calculates the number of unique sentences in the corpus. Options: yes, no. Default: no. NOTE: This is a bit more memory intensive, especially with larger corpora, so if you're only interested in token counts, set this to 'no'. 
In any case, running this script might take a while, depending on how large your corpus is.

Example command:

`python corpus_statistics.py -r no -u yes -c wn-corpus.1k.both.1ws.txt`


### Embeddings:

If you wish to use the generated random walk pseudo-corpora to train embeddings, you can do so, using your preferred embedding system. We simply used an off the shelf [pytorch](https://pytorch.org) implementation.

Our taxonomic embeddings, trained on the generated corpora provided above, can be downloaded [here](https://arrow.dit.ie/datas/12/).


### Word Similarity:

If you already have word embeddings you wish to evaluate, or you've downloaded ours, we provide a script that will calculate the word similarity based on your embeddings, across a any provided set of word pairs. The script calculates [cosine similarity](https://towardsdatascience.com/overview-of-text-similarity-metrics-3397c4601f50) between word vectors to provide a word similarity score.

Optionally, you can also use our script to concatenate different kinds of embeddings (e.g. [taxonomic](https://arrow.dit.ie/datas/12/) and [contextual](https://arrow.dit.ie/datas/11/)) and then use the product of the concatenation to compare similarity of a pair of words. This allows for the combination of different kinds of knowledge for more well-rounded representations (see papers below for more details).

To obtain a word similarity score, simply run our `predict_similarity.py` script to compare the similarity of a pair of words using your word embeddings.

The possible options and corresponding arguments are:

* --test : File name/location of your test file, i.e. the list of word pairs that are to be compared.
* --vecs1 : File name/location of your embedding, i.e. the idx2vec.dat file.
* --word2idx1 : File name/location of the word2idx.dat file corresponding to your embedding.
* --vecs2 : File name/location of your second embedding (idx2vec.dat). This is an optional argument and the script works without it.
* --word2idx2 : File name/location of the word2idx.dat file corresponding to your second embedding. This is an optional argument and the script works without it.
* --out : File name/location of the output file which will contain similarity results.
* --smwe : Sum multi-word expressions. This is turned off by default.
* --default : Use mean of matrix as default value if word is not found. This is turned off by default.

Example commands:

`python predict_similarity.py --vecs1 ./wn-corpus.1m.both.1ws/idx2vec-e30.dat --word2idx1 ./wn-corpus.1m.both.1ws/word2idx.dat --test simlex.data --out 1m.both.1ws.scores --smwe --default`

`python predict_similarity.py --vecs1 ./wn-corpus.1m.up.2ws/idx2vec-e30.dat --word2idx1 ./wn-corpus.1m.up.2ws/word2idx.dat --vecs2 ./wiki-corpus.009m/idx2vec-e30.dat --word2idx1 ./wiki-corpus.009m/word2idx.dat --test simlex.data --out wiki.009m+wn.1m.up.2ws.scores --smwe --default`


If you don't have your own set of word pairs that you want to measure for similarity, you might consult some of the following resources to obtain benchmark word similarity and word relatedness test sets:

* [SimLex-999](https://fh295.github.io/simlex.html)
* [WS-353](http://www.cs.technion.ac.il/~gabr/resources/data/wordsim353/)
* [SemEval-2017](http://alt.qcri.org/semeval2017/task2/index.php?id=data-and-tools)
* [Evocation Dataset](http://wordnet.cs.princeton.edu/downloads.html) - for something a little bit different

There you can also find similarity scores judged by humans, which allows you to calculate correlation scores between the performance of your embeddings and human judgement.


# Citation:

If you use any of the above code or data in your research, please cite the following paper(s):

```
@inproceedings{klubicka-etal-2020-english,
    title = "{E}nglish {W}ord{N}et Random Walk Pseudo-Corpora",
    author = "Klubi{\v{c}}ka, Filip and Maldonado, Alfredo and Mahalunkar, Abhijit and Kelleher, John",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    year = "2020",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2020.lrec-1.602"
}
```
You can download the paper [here](https://aclanthology.org/2020.lrec-1.602).

```
@inproceedings{klubicka2019synthetic,
  title="Synthetic, yet natural: Properties of WordNet random walk corpora and the impact of rare words on embedding performance",
  author="Filip Klubi\v{c}ka and Alfredo Maldonado and Abhijit Mahalunkar and John D. Kelleher",
  booktitle ="Proceedings of GWC: 10th Global Wordnet Conference",
  year="2019"
}
```
You can download the paper [here](https://arrow.dit.ie/cgi/viewcontent.cgi?article=1283&context=scschcomcon).

```
@article{maldonado2019size,
author="Maldonado, Alfredo
and Klubi{\v{c}}ka, Filip and Kelleher, John D.",
title="Size Matters: The Impact of Training Size in Taxonomically-Enriched Word Embeddings",
journal="Open Computer Science",
publisher="De Gruyter",
year="2019",
doi="doi.org/10.1515/comp-2019-0009"
}
```
You can download the paper [here](https://www.degruyter.com/document/doi/10.1515/comp-2019-0009/html).

This work has been funded by a grant from Science Foundation Ireland: Grant Number 13/RC/2106.

# Licensing information:

Copyright © 2019 Filip Klubička, Alfredo Maldonado. Technological University Dublin, ADAPT Centre.
All Rights Reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

