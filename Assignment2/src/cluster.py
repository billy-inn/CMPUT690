
if __name__ == "__main__":
	print "Stage 3: Clustering starts!"

	infile1 = open("../output/raw_relation.tsv")
	infile2 = open("../output/entity.txt")
	#outfile = open("../output/test3.tsv", "w")
	outfile = open("../output/cmput690w16a2_Xu.tsv", "w")
	relationSet = set()
	c0 = 0; c1 = 0; c2 = 0; c3 = 0; c4 = 0; c5 = 0; c6 = 0
	c7 = 0; c8 = 0; c9 = 0; c10 = 0; c11 = 0; c12 = 0; c13 = 0
	for line in infile1.readlines():
		e1, pattern, e2, ad = line.split('\t')
		ad = int(ad.strip())
		relation = -1
		if "play" in pattern:
			if "for" in pattern:
				relation = "play for"
				c1 += 1
			elif ("in" in pattern) or ("from" in pattern):
				relation = "play in"
				if "in" in pattern:
					c2 += 1
				else:
					c0 += 1
			elif "ORGANIZATION" in e2:
				relation = "play for"
				c1 += 1
			elif "LOCATION" in e2:
				c2 += 1
				relation = "play in"
		if "born" in pattern:
			c3 += 1
			relation = "born in"
		if pattern == "in ":
			c4 += 1
			relation = "locate in"
		if "base" in pattern:
			c5 += 1
			relation = "locate in"
		if "locate" in pattern:
			c6 += 1
			relation = "locate in"
		if "found" in pattern:
			c7 += 1
			relation = "found by"
		if "designed by" in pattern:
			c8 += 1
			relation = "designed by"
		if "refer" in pattern:
			c9 += 1
			relation = "refer as"
		if "known" in pattern:
			c10 += 1
			relation = "refer as"
		if "abbreviated to" in pattern:
			c11 += 1
			relation = "refer as"
		if ("nickname" in pattern) and ("PERSON" in e1) and ("PERSON" in e2):
			c12 += 1
			relation = "refer as"
		if pattern == "simply ":
			c13 += 1
			relation = "refer as"
		if relation != -1:
			relationSet.add((e1, relation, e2, ad))
	entityDict = {}
	for entity in infile2.readlines():
		label, instance = entity.strip().split('\t')
		entityDict[label] = instance
	sorted_relation = sorted(list(relationSet), key=lambda x: x[3])
	for relation in sorted_relation:
		outfile.write("%s\t%s\t%s\t%d\n" % (entityDict[relation[0]], relation[1], entityDict[relation[2]], relation[3]))

	print "Completed!!!"
