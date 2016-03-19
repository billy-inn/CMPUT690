from gensim.models import Word2Vec
import re
from nltk.corpus import stopwords
import logging

def doc2wordlist(doc, remove_stopwords=False):
	text = re.sub("[^a-zA-Z0-9]", " ", doc)
	words = text.lower().split()
	if remove_stopwords:
		stops = set(stopwords.words("english"))
		words = [w for w in words if not w in stops]
	return words

if __name__ == '__main__':
	corpus = []
	count = 826
	for i in range(1, count+1):
		infile = open("../data/transformed_%d.txt" % i)
		text = doc2wordlist(infile.read(), True)
		infile.close()
		corpus.append(text)

	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
			level=logging.INFO)

	num_features = 400
	min_word_count = 1
	num_workers = 4
	context = 10
	downsampling = 1e-3
	
	model = Word2Vec(corpus, workers=num_workers, \
				size=num_features, min_count=min_word_count, \
				window=context, sample=downsampling, seed=1)
	model.init_sims(replace=True)
	model_name = "../model/word2vec.1"
	model.save(model_name)

