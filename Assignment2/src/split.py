infile = open("../cmput690a1_documents.txt")
# infile = open("../sample.txt")
corpus = infile.readlines()
infile.close()
counter = 0
for document in corpus:
	document = document.replace('\\n', '\n')
	outfile = open("../data/%d.txt" % counter, "w")
	# outfile = open("../sample_data/%d.txt" % counter, "w")
	outfile.write(document)
	outfile.close()
	counter += 1
