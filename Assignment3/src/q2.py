import rdflib.graph as g

if __name__ == "__main__":
	G = g.Graph()
	G.parse("../cmput690_a3.ttl", format="n3")
	infile = open("../output/doc.txt")
	entitySet = set()
	for line in infile.readlines():
		entitySet.add(line.strip())
	q = open("q2.rq").read()
	results = G.query(q)
	outfile = open("../output/q2.tsv", "w")
	outfile2 = open("../output/player.txt", "w")
	outfile3 = open("../output/team.txt", "w")
	playerSet = set()
	teamSet = set()
	for row in results:
		outfile.write("%s\t%s\n" % (row[0], row[1]))
		playerSet.add(row[0])
		teamSet.add(row[1])
	for player in playerSet:
		outfile2.write("%s\n" % player)
	for team in teamSet:
		outfile3.write("%s\n" % team)
