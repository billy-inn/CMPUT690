import rdflib.graph as g
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from SPARQLWrapper import SPARQLWrapper, JSON

if __name__ == "__main__":
	endpoint = SPARQLWrapper("http://dbpedia.org/sparql")
	endpoint.setReturnFormat(JSON)

	G = g.Graph()
	G.parse("../cmput690_a3.ttl", format="n3")
	infile = open("../output/stadium.tsv")
	stadiumSet = set()
	for line in infile.readlines():
		stadium, text = line.split('\t')
		stadiumSet.add(stadium)
	infile.close()
	infile = open("../output/team2stadium.tsv")
	outfile = open("../output/q1.tsv", "w")
	for line in infile.readlines():
		team, stadium = line.strip().split("\t")
		endpoint.setQuery('''
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?entity WHERE {
	<%s> owl:sameAs ?entity.
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
		#sub = URIRef("http://rdf.freebase.com/ns/" + player)
		#pred = URIRef("http://rdf.freebase.com/key/nation")
		#obj = Literal(nation)
		#G.add((sub, pred, obj))
	#q = open("q1.rq").read()
	#results = G.query(q)
	#outfile = open("../output/q1.tsv", "w")
	#for row in results:
	#	outfile.write("%s\t%s\n" % (row[0], row[1]))
		#outfile.write("%s\n" % row[0])
