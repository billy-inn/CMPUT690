
infile = open("ruleBased.txt")
labelDict = {}
for item in infile.readlines():
	label, instance, idx = item.split('\t')
	if not labelDict.has_key(label):
		labelDict[label] = 1
	else:
		labelDict[label] += 1

for key in labelDict.keys():
	print key, labelDict[key]

