from nltk.tag import StanfordNERTagger
from nltk import word_tokenize
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')

outfile = open("../output/entity.txt", "w")
doc_count = 826
entitySet = {}
print "Stage 1: NER starts!"
for i in range(doc_count):
	infile = open("../data/%d.txt" % i)
	tags = st.tag(word_tokenize(unicode(infile.read())))
	infile.close()
	transform_file = open("../data/transformed_%d.txt" % i, "w")
	entity = u''
	label = u''
	transform_text = u''
	if i % 10 == 0:
		print "%d files have been processed." % i 
	for tag in tags:
		if tag[1] == u'O':
			if label != u'':
				if not entitySet.has_key((entity, label)):
					entitySet[(entity, label)] = len(entitySet)
					outfile.write('%s%d\t%s\n' % (label, entitySet[(entity, label)], entity))
				transform_text += ' %s%d' % (label, entitySet[(entity, label)])
			transform_text += ' ' + tag[0]
			entity = ''
			label = ''
		elif entity == u'':
			entity = tag[0]
			label = tag[1]
		elif label == tag[1]:
			entity += u' ' + tag[0]
		else:
			if not entitySet.has_key((entity, label)):
				entitySet[(entity, label)] = len(entitySet)
				outfile.write('%s%d\t%s\n' % (label, entitySet[(entity, label)], entity))
			transform_text += ' %s%d' % (label, entitySet[(entity, label)])
			entity == tag[0]
			label = tag[1]
	transform_file.write("%s\n" % transform_text[1:])
