print "Coreference Resolution starts!"

infile = open("../utils/coreference.txt")
entityDict = {}
for line in infile.readlines():
	idx, entity = line.split('\t')
	if not entityDict.has_key(idx):
		entityDict[idx] = [entity.strip()]
	else:
		entityDict[idx].append(entity.strip())

outfile = open("../output/CR.txt", "w")
for key in entityDict.keys():
	entityList = entityDict[key]
	if len(entityList) > 1:
		entity = entityList[0].lower().split()
		coreference = []
		for e in entityList[1:]:
			words = e.lower().split()
			for word in words:
				if word in entity:
					coreference.append(e)
					break
		if len(coreference):
			outfile.write("%s(%d)" % (entityList[0], int(key)))
			for c in coreference:
				outfile.write(",%s(%d)" % (c, int(key)))
			outfile.write("\n")
			
