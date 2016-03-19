import rdflib.graph as g
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace

if __name__ == "__main__":
	G = g.Graph()
	G.parse("../cmput690_a3.ttl", format="n3")
	infile = open("../output/nation.tsv")
	for line in infile.readlines():
		player, nation = line.strip().split("\t")
		sub = URIRef("http://rdf.freebase.com/ns/" + player)
		pred = URIRef("http://rdf.freebase.com/key/nation")
		obj = Literal(nation)
		G.add((sub, pred, obj))
	infile.close()
	infile = open("../output/q2.tsv")
	for line in infile.readlines():
		player, team = line.strip().split("\t")
		sub = URIRef(team)
		pred = URIRef("http://rdf.freebase.com/key/player_list")
		obj = URIRef(player)
		G.add((sub, pred, obj))
	infile.close()
	infile = open("../output/coach.tsv")
	for line in infile.readlines():
		coach, team = line.strip().split("\t")
		sub = URIRef(team)
		pred = URIRef("http://rdf.freebase.com/key/coached_by")
		obj = URIRef(coach)
		G.add((sub, pred, obj))
	infile.close()
	q = open("q3.rq").read()
	results = G.query(q)
	outfile = open("../output/q3.tsv", "w")
	for row in results:
		#outfile.write("%s\t%s\n" % (row[0], row[1]))
		outfile.write("%s\n" % row[0])
