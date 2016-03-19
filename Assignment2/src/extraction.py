from nltk.parse.stanford import StanfordDependencyParser
from nltk import pos_tag
import re
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getLCA(G, root, e1, e2):
	if (root == e1) or (root == e2):
		return root
	if not G.has_key(root):
		return 0
	nodeList = []
	for child in G[root]:
		node = getLCA(G, child, e1, e2)
		if node != 0:
			nodeList.append(node)
	if len(nodeList) > 1:
		return root
	elif len(nodeList) == 1:
		return nodeList[0]
	else:
		return 0

if __name__ == '__main__':
	dep_parser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz");

	entityfile = open("../output/entity.txt")
	entityDict = {}
	for entity in entityfile.readlines():
		label, instance = entity.strip().split('\t')
		entityDict[label] = instance

	#outfile = open("../output/cmput690w16a2_Xu.tsv", "w")
	outfile = open("../output/raw_relation.tsv", "w")
	doc_count = 826
	#doc_count = 1
	#reg = r'((PERSON)(\d)+)|(LOCATION(\d)+)|(ORGANIZATION(\d)+)'
	reg = r'PERSON\d+|LOCATION\d+|ORGANIZATION\d+'
	regex = re.compile(reg)
	noun_tag = set(['NN', 'NNS', 'NNP', 'NNPS'])
	verb_tag = set(['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'])

	print "Stage 2: Extraction starts!"
	for k in range(doc_count):
	#for k in range(100, 110):
		if k % 10 == 0:
			print "%d files have been processed!" % k

		infile = open("../data/transformed_%d.txt" % k)
		#infile = open("../test.txt")
		sentences = infile.read().split(' . ')
		# omit the truncated sentence
		if sentences[-1].strip()[-1] != '.':
			sentences = sentences[:-1]
		if len(sentences) == 0:
			continue

		left = sentences[0].find('(')
		right = sentences[0].find(')')
		firstSentence = []
		if (left != -1) and (right != -1):
			firstSentence.append(sentences[0][:left-1] + sentences[0][left+1:right])
			firstSentence.append(sentences[0][:left-1] + sentences[0][right+1:])
		else:
			firstSentence.append(sentences[0])

		for sentence in firstSentence:
			words = sentence.strip().split()
			postags = pos_tag(words)
			Distinct = {}
			for i in range(len(words)):
				tmp = words[i]
				while Distinct.has_key(words[i]):
					words[i] += '0'
				if (postags[i][1] == 'IN') or (postags[i][1] == 'DT') or (postags[i][0] in string.punctuation):
					Distinct[tmp] = tmp
					words[i] = tmp
				else:
					Distinct[words[i]] = tmp
			#print Distinct
			sentence = ""
			for word in words:
				if word in string.punctuation:
					continue
				sentence += word + " "
			sentence = sentence.strip()

			entityList = re.findall(regex, sentence)
			N = len(entityList)
			if N > 1:
				#print sentence
				edges = [list(parse.triples()) for parse in dep_parser.raw_parse(sentence)]
				#print edges
				G = {}
				relation = {}
				case = {}
				POS = {}
				Pa = {}
				for edge in edges[0]:
					POS[edge[0][0]] = edge[0][1]
					POS[edge[2][0]] = edge[2][1]
					if edge[1] == 'det':
						continue
					if edge[1] == 'case':
						case[edge[0][0]] = edge[2][0]
						continue
					relation[(edge[0][0], edge[2][0])] = edge[1];
					if G.has_key(edge[0][0]):
						G[edge[0][0]].append(edge[2][0])
					else:
						G[edge[0][0]] = [edge[2][0]]
					Pa[edge[2][0]] = edge[0][0]
				root = edges[0][0][0][0]
				for i in range(N):
					for j in range(i+1, N):
						e1 = entityList[i]
						e2 = entityList[j]
						#if e1[0] == e2[0]:
						#	continue
						node = getLCA(G, root, e1, e2)
						#print node, e1, e2
						words1 = []
						e = e1
						while e != node:
							words1.append(e)
							e = Pa[e]
						words2 = [e2]
						if case.has_key(e2):
							words2.append(case[e2])
						e = e2
						while e != node:
							e = Pa[e]
							words2.append(e)
						words = words1 + words2[::-1]
						text = ""
						verb_count = 0
						for word in words[1:-1]:
							if POS[word] in noun_tag:
								if (word != e1) and (word != e2):
									continue
							if POS[word] in verb_tag:
								verb_count += 1
							#text += word + "(%s) " % POS[word]
							if Distinct.has_key(word):
								text += Distinct[word] + " "
							else:
								text += word + " "
						#if verb_count <= 1:
						if verb_count <= 1:
							#outfile.write('%s\n' % text)
							#outfile.write("%s\t%s\t%s\t%d\n" % (entityDict[Distinct[e1]], text, entityDict[Distinct[e2]], k))
							outfile.write("%s\t%s\t%s\t%d\n" % (Distinct[e1], text, Distinct[e2], k))
	
