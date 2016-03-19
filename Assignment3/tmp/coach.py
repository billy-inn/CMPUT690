import rdflib.graph as g

if __name__ == "__main__":
	G = g.Graph()
	G.parse("../cmput690_a3.ttl", format="n3")
	q = open("coach.rq").read()
	results = G.query(q)
	outfile = open("../output/coach.tsv", "w")
	for row in results:
		outfile.write("%s\t%s\n" % (row[0], row[1]))
