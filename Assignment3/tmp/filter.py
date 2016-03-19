import rdflib.graph as g

if __name__ == "__main__":
	G = g.Graph()
	G.parse("../cmput690_a3.ttl", format="n3")
	q = open("withDoc.rq").read()
	results = G.query(q)
	outfile = open("../output/doc.txt", "w")
	for row in results:
		outfile.write("%s\n" % row[0])

