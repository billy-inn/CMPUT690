import rdflib.graph as g
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from SPARQLWrapper import SPARQLWrapper, JSON

if __name__ == "__main__":
	endpoint = SPARQLWrapper("http://dbpedia.org/sparql")
	endpoint.setReturnFormat(JSON)

	print "Graph Construction Starts!"
	G = g.Graph()
	G.parse("../cmput690_a3.ttl", format="n3")

	# Add relation: ?player fbk:nation ?nation
	infile = open("../output/nation.tsv")
	for line in infile.readlines():
		player, nation = line.strip().split('\t')
		sub = URIRef("http://rdf.freebase.com/ns/" + player)
		pred = URIRef("http://rdf.freebase.com/key/nation")
		obj = Literal(nation)
		G.add((sub, pred, obj))
	infile.close()

	# Add relation: ?team fbk:player_list ?player
	infile = open("../output/q2.tsv")
	for line in infile.readlines():
		player, team = line.strip().split("\t")
		sub = URIRef(team)
		pred = URIRef("http://rdf.freebase.com/key/player_list")
		obj = URIRef(player)
		G.add((sub, pred, obj))
	infile.close()
	
	# Add relation: ?team fbk:coached_by ?coach
	infile = open("../output/coach.tsv")
	for line in infile.readlines():
		coach, team = line.strip().split("\t")
		sub = URIRef(team)
		pred = URIRef("http://rdf.freebase.com/key/coached_by")
		obj = URIRef(coach)
		G.add((sub, pred, obj))
	infile.close()

	infile = open("../output/stadium.tsv")
	stadiumSet = set()
	for line in infile.readlines():
		stadium, text = line.split('\t')
		stadiumSet.add(stadium)
	infile.close()

	# Answer Question 1
	print "Question 1 Answering starts!"
	infile = open("../output/team2stadium.tsv")
	outfile = open("../output/cmput690w16a3_q1_Xu.tsv", "w")
	for line in infile.readlines():
		team, stadium = line.strip().split('\t')
		endpoint.setQuery('''
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?entity WHERE {
	<%s> owl:sameAs ?entity .
}
''' % stadium)
		results = endpoint.query().convert()
		if len(results["results"]["bindings"]) == 0:
			continue
		for res in results["results"]["bindings"]:
			if "freebase" in res["entity"]["value"]:
				entity = res["entity"]["value"]
				if entity in stadiumSet:
					outfile.write("%s\t%s\n" % (entity, team))
				break
	infile.close()
	outfile.close()
	
	# Answer Question 2
	print "Question 2 Answering starts!"
	q = open("q2.rq").read()
	results = G.query(q)
	outfile = open("../output/cmput690w16a3_q2_Xu.tsv", "w")
	for row in results:
		outfile.write("%s\t%s\n" % (row[0], row[1]))
	outfile.close()

	# Answer Question 3
	print "Question 3 Answering starts!"
	q = open("q3.rq").read()
	results = G.query(q)
	outfile = open("../output/cmput690w16a3_q3_Xu.tsv", "w")
	for row in results:
		outfile.write("%s\n" % row[0])
	outfile.close()

	# Answer Question 4
	print "Question 4 Answering starts!"
	infile = open("../output/cmput690w16a3_q1_Xu.tsv")
	stadium2team = {}
	for line in infile.readlines():
		stadium, team = line.strip().split('\t')
		stadium2team[stadium] = team
	infile.close()

	infile = open("../output/stadium.tsv")
	outfile = open("../output/cmput690w16a3_q4_Xu.tsv", "w")
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
					outfile.write("%s\n" % stadium2team[stadium])
	outfile.close()
	infile.close()

	# Answer Question 5
	print "Question 5 Answering starts!"
	q = open("q5.rq").read()
	results = G.query(q)
	outfile = open("../output/cmput690w16a3_q5_Xu.tsv", "w")
	for row in results:
		outfile.write("%s\t%s\n" % (row[0], row[1]))
	outfile.close()

