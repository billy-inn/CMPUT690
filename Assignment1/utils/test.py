from nltk import word_tokenize
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

doc_count = 826
pattern = 0
for i in range(1, doc_count + 1):
	infile = open("data/%d.txt" % i)
	text = unicode(infile.read())
	sentences = [word_tokenize(sentence) for sentence in re.split('\.\s', text)]
	firstSentence = sentences[0]
	if u'is' in sentences[0]:
		pattern += 1
	elif u'are' in sentences[0]:
		pattern += 1
	elif u'was' in sentences[0]:
		pattern += 1
	else:
		print i
print pattern
