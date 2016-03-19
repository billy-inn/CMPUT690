from SPARQLWrapper import SPARQLWrapper, JSON

endpoint = SPARQLWrapper("http://dbpedia.org/sparql")

endpoint.setReturnFormat(JSON)

infile = open("../output/doc.txt")
outfile = open("../output/fb2db.txt", "w")
for line in infile.readlines():
	endpoint.setQuery('''
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX freebase: <http://rdf.freebase.com/ns/>

SELECT ?entity WHERE {
	  ?entity owl:sameAs freebase:%s .
}
''' % line.strip()[27:])
	results = endpoint.query().convert()
	print line.strip()
	outfile.write("%s\t" % line.strip())
	if len(results["results"]["bindings"]) == 0:
		print "NA"
	else:
		print results["results"]["bindings"][0]["entity"]["value"]
		outfile.write("%s\n" % results["results"]["bindings"][0]["entity"]["value"])
	print "--------------------"
