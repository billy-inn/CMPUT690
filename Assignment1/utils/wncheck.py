from nltk.corpus import wordnet as wn
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

outfile = open('wncheck.txt', 'w')

def wncheck(x):
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
	if len(sets):
		outfile.write('%s: %s\n' % (x, label))

infile = open("baseline.txt")
for item in infile.readlines():
	label, entity, idx = item.split('\t')
	if label == "LOCATION":
		wncheck(entity)

