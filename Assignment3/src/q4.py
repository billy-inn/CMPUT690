from nltk import word_tokenize
import rdflib.graph as g

G = g.Graph()
G.parse("../cmput690_a3.ttl", format="n3")

infile = open("../output/q1.tsv")
stadium2team = {}
for line in infile.readlines():
	stadium, team = line.strip().split('\t')
	stadium2team[stadium] = team
infile.close()

infile = open("../output/stadium.tsv")
outfile = open("../output/q4.tsv", "w")
for line in infile.readlines():
	stadium, text = line.split('\t')
	results = G.query('''
PREFIX c690: <http://cmput690/>

SELECT ?doc WHERE {
	  <%s> c690:hasDocument ?doc .
}
''' % stadium)
	for row in results:
		sentences = row[0].split('.')
		for sentence in sentences:
			idx1 = sentence.find("named")
			offset1 = 5
			if idx1 == -1:
				continue
			idx2 = sentence[idx1+offset1:].find("after")
			offset2 = 5
			if idx2 == -1:
				idx2 = sentence[idx1+offset1:].find("in honour of")
				offset2 = 11
			if idx2 == -1:
				continue
			if ("president" in sentence[idx2+offset2:]) or ("chairman" in sentence[idx2+offset2:]):
				print sentence
				print stadium
				print stadium2team[stadium]
				print "---------"
				outfile.write("%s\n" % stadium2team[stadium])

