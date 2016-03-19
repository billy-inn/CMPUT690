from SPARQLWrapper import SPARQLWrapper, JSON

endpoint = SPARQLWrapper("http://dbpedia.org/sparql")
endpoint.setReturnFormat(JSON)

print "Starts Extracting Teams to Stadiums!"
infile = open("../output/team.txt")
outfile = open("../output/team2stadium.tsv", "w")
for line in infile.readlines():
	team = line.strip()
	endpoint.setQuery('''
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX freebase: <http://rdf.freebase.com/ns/>

SELECT ?entity WHERE {
	  ?entity owl:sameAs freebase:%s .
}
''' % team[27:])
	results = endpoint.query().convert()
	if len(results["results"]["bindings"]) == 0:
		continue
	for res in results["results"]["bindings"]:
		entity = res["entity"]["value"]
		endpoint.setQuery('''
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?stadium WHERE {
	  { <%s> dbo:ground ?stadium . }
	  UNION
	  { <%s> dbp:ground ?stadium . }
	  { ?stadium rdf:type dbo:Stadium . }
	  UNION
	  { ?stadium rdf:type <http://dbpedia.org/class/yago/Stadium104295881> . }
}
''' % (entity, entity))
		country = endpoint.query().convert()
		if len(country["results"]["bindings"]) == 0:
			continue
		for c in country["results"]["bindings"]:
			print team[27:], c["stadium"]["value"]
			outfile.write("%s\t%s\n" % (team, c["stadium"]["value"]))
		break
