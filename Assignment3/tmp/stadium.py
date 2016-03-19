import rdflib.graph as g
from nltk.tag import StanfordNERTagger
from nltk import word_tokenize, pos_tag
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def check(x):
	words = x.split()
	flag = False
	for word in words:
		if word == u"stadium":
			flag = True
			break
		if word == u"ground":
			flag = True
			break
	return flag

if __name__ == "__main__":
	StanfordNERPath = './stanford-ner'
	st = StanfordNERTagger(StanfordNERPath + '/classifiers/english.all.3class.distsim.crf.ser.gz', StanfordNERPath + '/stanford-ner.jar')

	indicator = set([u'is', u'was', u'are', u'were'])
	noun_tag = set(['NN', 'NNS', 'NNP', 'NNPS'])

	G = g.Graph()
	G.parse("../cmput690_a3.ttl", format="n3")
	q = open("withDoc.rq").read()
	results = G.query(q)
	outfile = open("../output/stadium.tsv", "w")
	count = 0
	for row in results:
		count += 1
		if count % 10 == 0:
			print count
		text = row[1]
		tags = st.tag(word_tokenize(text))
		firstSentence = ''
		for j in range(1, len(text)):
			if (text[j] == '.') and ((j+1==len(text) or (text[j+1] in string.whitespace))):
				if text[j-1] not in string.uppercase:
					firstSentence = text[:j]
					break
		if firstSentence == '':
			firstSentence = text.split('.')[0]
		postags = pos_tag(word_tokenize(firstSentence))
		posLen = len(postags)
		noun = ''
		idx = 0
		for j in range(posLen):
			if postags[j][0] in indicator:
				idx = j
				for k in range(j+1, posLen):
					if postags[k][1] in noun_tag:
						if noun == '':
							noun = postags[k][0]
						else:
							noun += ' ' + postags[k][0]
				break
		flag = check(noun)
		if flag == False:
			continue
		print firstSentence
		outfile.write("%s\t%s\n" % (row[0], firstSentence))
