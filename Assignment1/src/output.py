from nltk.tag import StanfordNERTagger
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

StanfordNERPath = './stanford-ner'

st = StanfordNERTagger(StanfordNERPath + '/classifiers/english.all.3class.distsim.crf.ser.gz', StanfordNERPath + '/stanford-ner.jar')

outfile = open("../output/cmput690w16a1_Xu.tsv", "w")
outfile2 = open("../utils/coreference.txt", "w")
doc_count = 826
entitySet = set()
indicator = set([u'is', u'was', u'are', u'were'])
noun_tag = set(['NN', 'NNS', 'NNP', 'NNPS'])
soccer_player = set(['footballer', 'player', 'defender', 'forward', 'player', 'midfielder', 'striker', 'goalkeeper'])
soccer_team = set(['club', 'team'])
stadium = set(['stadium'])

def check(x, y, z, idx):
	#print x, y, z, idx
	words = x.split()
	flag = False
	if z == 'PERSON':
		for word in words:
			if word in soccer_player:
				flag = True
				break
		if flag:
			outfile.write('soccer_player\t%s\t%d\n' % (y, idx))
			outfile2.write('%d\t%s\n' % (idx, y))
			#print idx + 1, y
	elif z == 'ORGANIZATION':
		for word in words:
			if word in soccer_team:
				flag = True
				break
		if flag:
			outfile.write('soccer_team\t%s\t%d\n' % (y, idx))
			outfile2.write('%d\t%s\n' % (idx, y))
	elif z == 'LOCATION':
		for word in words:
			if word in stadium:
				flag = True
				break
		if flag:
			outfile.write('stadium\t%s\t%d\n' % (y, idx))
			outfile2.write('%d\t%s\n' % (idx, y))
	#if flag:
	#	print 'Yes:', idx, y

def wncheck(x, idx):
	sets = wn.synsets(x)
	label = ''
	for s in sets:
		text = s.definition().lower().split()
		if ('city' in text) or ('capital' in text):
			label = 'city'
		elif ('country' in text) or ('republic' in text) or ('monarchy' in text) or ('kingdom' in text) or ('nation' in text):
			label = 'country'
		elif 'state' in text:
			label = 'state'
		else:
			continue
		break
	if label != '':
		outfile.write('%s\t%s\t%d\n' % (label, x, idx))

print "Improved method starts!"
for i in range(1, doc_count + 1):
	infile = open("../data/%d.txt" % i)
	text = unicode(infile.read())
	infile.close()
	tags = st.tag(word_tokenize(text))
	firstSentence = ''
	for j in range(1, len(text)):
		if (text[j] == '.') and (text[j+1] in string.whitespace):
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
	if i % 10 == 0:
		print "%d files have been processed" % i
	entity = u''
	label = u''
	for j in range(len(tags)):
		tag = tags[j]
		if tag[1] == u'O':
			if label != u'':
				if (entity, label) not in entitySet:
					entitySet.add((entity, label))
					outfile.write("%s\t%s\t%d\n" % (label.lower(), entity, i-1))
					if j <= idx:
						check(noun, entity, label, i-1)
					if label == "LOCATION":
						wncheck(entity, i-1)
			entity = ''
			label = ''
		elif entity == u'':
			entity = tag[0]
			label = tag[1]
		elif label == tag[1]:
			entity += u' ' + tag[0]
		else:
			if (entity, label) not in entitySet:
				entitySet.add((entity, label))
				outfile.write("%s\t%s\t%d\n" % (label.lower(), entity, i-1))
				if j <= idx:
					check(noun, entity, label, i-1)
				if label == "LOCATION":
					wncheck(entity, i-1)
			entity == tag[0]
			label = tag[1]
