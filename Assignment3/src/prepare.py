from SPARQLWrapper import SPARQLWrapper, JSON
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
	endpoint = SPARQLWrapper("http://dbpedia.org/sparql")
	endpoint.setReturnFormat(JSON)

	G = g.Graph()
	G.parse("../cmput690_a3.ttl", format="n3")

	# Get the entities of player and team
	print "Start Extracting Players and Teams!"
	outfile = open("../output/q2.tsv", "w")
	outfile1 = open("../output/player.txt", "w")
	outfile2 = open("../output/team.txt", "w")
	q = open("q2.rq").read()
	results = G.query(q)
	playerSet = set()
	teamSet = set()
	for row in results:
		outfile.write("%s\t%s\n" % (row[0], row[1]))
		playerSet.add(row[0])
		teamSet.add(row[1])
	for player in playerSet:
		outfile1.write("%s\n" % player)
	for team in teamSet:
		outfile2.write("%s\n" % team)
	outfile.close()
	outfile1.close()
	outfile2.close()

	# Get the relations between team and coach
	print "Starts Extracting Coaches!"
	q = open("coach.rq").read()
	results = G.query(q)
	outfile = open("../output/coach.tsv", "w")
	for row in results:
		outfile.write("%s\t%s\n" % (row[0], row[1]))
	outfile.close()

	# Get the entities of stadium
	print "Start Identifying Stadiums!"
	StanfordNERPath = './stanford-ner'
	st = StanfordNERTagger(StanfordNERPath + '/classifiers/english.all.3class.distsim.crf.ser.gz', StanfordNERPath + '/stanford-ner.jar')

	indicator = set([u'is', u'was', u'are', u'were'])
	noun_tag = set(['NN', 'NNS', 'NNP', 'NNPS'])

	q = open("withDoc.rq").read()
	results = G.query(q)
	outfile = open("../output/stadium.tsv", "w")
	count = 0
	for row in results:
		count += 1
		if count % 10 == 0:
			print "%d documents has been processed" % count
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
		outfile.write("%s\t%s\n" % (row[0], firstSentence))
	outfile.close()
