import rdflib.graph as g

if __name__ == "__main__":
	G = g.Graph()
	G.parse("../cmput690_a3.ttl", format="n3")
	infile = open("../output/doc.txt")
	outfile = open("../output/pred.txt", "w")
	count = 0
	for line in infile.readlines():
		entity = line.strip()[27:]
		#print entity
		q = '''PREFIX fb: <http://rdf.freebase.com/ns/>
PREFIX fbk: <http://rdf.freebase.com/key/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX c690: <http://cmput690/>

SELECT ?pred
WHERE
  {
	  fb:%s ?pred ?obj .
  }''' % entity
		res = G.query(q)
		outfile.write("%s" % entity)
		for row in res:
			#print row[0]
			count += 1
			outfile.write("\t%s" % row[0])
		outfile.write("\n")
		#print "------------------"
	print count
