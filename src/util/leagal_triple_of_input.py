#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:leagal_triple_of_input
   Author:jason
   date:2018/4/13
-------------------------------------------------
   Change Activity:2018/4/13:
-------------------------------------------------
"""
'''
获取输入格式的文件中合法的三元组信息，保存到指定文件中
'''

from nltk import ngrams


def convertBIO2one(sent):
	rst = []
	nidx = 0
	ntoken = ''
	ntag = ''
	# print(sent)
	for idx, token, bio in sent:
		if bio.startswith('B-'):
			nidx = idx
			ntoken = token
			ntag = bio[2:]
			rst.append((nidx, ntoken, ntag))
		elif bio.startswith('I-'):
			ntoken += token
			ntag = bio[2:]
		else:
			rst.append((nidx, ntoken, ntag))
			ntoken = ''
			ntag = ''
			nidx = idx
		print(rst)
		return rst
	
	def extract_triples(sents):
		triples = []  # e1, rel, e2
		for sent in sents:
			if sent == []:
				continue
			entities_of_sent = []
			relations_of_sent = []
			for i, tpl in enumerate(sent):
				token, tag = tpl
				if tag.endswith('REL'):
					relations_of_sent.append((i, token, tag))
				else:
					entities_of_sent.append((i, token, tag))
			# print(relations)
			# print(entities)
			if entities_of_sent == [] or relations_of_sent == []:
				continue
			relations = convertBIO2one(relations_of_sent)
		# entities_bgrams = ngrams(convertBIO2one(entities_of_sent), 2)
		# for bgram in entities_bgrams:
		# 	print(bgram)
		
		return triples
	
	delimiter = '\t'
	
	if __name__ == '__main__':
		input = "../../data/input/input1.txt.utf-8"
		output = "../../data/triple_from_input/triples.txt"
		
		text = []
		with open(input, 'r', encoding='utf-8') as f:
			text = f.readlines()
		
		sents = []
		sent = []
		for line in text:
			ts = line.split(delimiter)
			token = ts[0].strip()
			target = ts[len(ts) - 1].strip()
			if target.strip() != 'O':
				if token == '':
					sents.append(sent)
					sent = []
				else:
					sent.append((token, target))
		# print(token, target)
		# print(len(sents))
		# for s in sents:
		# print(s)
		
		triples = extract_triples(sents)

# with open(output, 'w', encoding='utf-8') as f:
# 	for triple in triples:
# 		f.write(','.join(triple))
# 		f.write("\n")
