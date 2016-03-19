

if __name__ == "__main__":
	infile = open("test1.tsv")
	outfile = open("test2.tsv", "w")
	for line in infile.readlines():
		item = line.split('\t')
		pattern = item[1]
		if "play" in pattern:
			if "in" in pattern:
				continue
			if "from" in pattern:
				continue
			if "for" in pattern:
				continue
			print pattern
			continue
		if "locate" in pattern:
			continue
		if "born" in pattern:
			continue
		if "known" in pattern:
			continue
		if "in" in pattern:
			continue
		if len(pattern) == 0:
			continue
		if "base" in pattern:
			continue
		outfile.write("%s" % line)
