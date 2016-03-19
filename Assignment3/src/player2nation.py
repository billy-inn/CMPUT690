from SPARQLWrapper import SPARQLWrapper, JSON

endpoint = SPARQLWrapper("http://dbpedia.org/sparql")
endpoint.setReturnFormat(JSON)

print "Starts Extracting Players to Nations!"
infile = open("../output/player.txt")
outfile = open("../output/nation.tsv", "w")
for line in infile.readlines():
	player = line.strip()
	endpoint.setQuery('''
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX freebase: <http://rdf.freebase.com/ns/>

SELECT ?entity WHERE {
	  ?entity owl:sameAs freebase:%s .
}
''' % player[27:])
	results = endpoint.query().convert()
	if len(results["results"]["bindings"]) == 0:
		continue
	for res in results["results"]["bindings"]:
		entity = res["entity"]["value"]
		endpoint.setQuery('''
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?country_name WHERE {
	  <%s> dbo:birthPlace/dbo:country ?country .
	  ?country rdfs:label ?country_name .
	  FILTER (LANG(?country_name) = 'en') .
}
''' % entity)
		country = endpoint.query().convert()
		if len(country["results"]["bindings"]) == 0:
			continue
		for c in country["results"]["bindings"]:
			print player[27:], c["country_name"]["value"]
			outfile.write("%s\t%s\n" % (player[27:], c["country_name"]["value"]))
		break
