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


def convertRELBIO2one(sent):
	indexs = [i for i, w, t in sent if t.startswith('B-')]
	tokens = []
	for idx, token, tag in sent:
		if tag.startswith('I-'):  # Inside NE
			tokens[-1] += ' ' + token
		elif tag.startswith('B-'):  # Adjacent NE
			tokens.append(token)
	
	return [(i, t) for i, t in zip(indexs, tokens)]


def convertEntBIO2one(sent):
	index_tags = [[i, t[2:]] for i, w, t in sent if t.startswith('B-')]
	tokens = []
	for idx, token, tag in sent:
		if tag.startswith('I-'):  # Inside NE
			tokens[-1] += ' ' + token
		elif tag.startswith('B-'):  # Adjacent NE
			tokens.append(token)
	
	return [(i_t[0], w, i_t[1]) for i_t, w in zip(index_tags, tokens)]


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
		# print(entities_of_sent)
		if entities_of_sent == [] or relations_of_sent == []:
			continue
		relations = convertRELBIO2one(relations_of_sent)
		# print(relations_of_sent)
		# print(relations)
		# print(convertEntBIO2one(entities_of_sent))
		entities_bgrams = list(ngrams(convertEntBIO2one(entities_of_sent), 2))
		# print(entities_of_sent)
		# print(entities_bgrams)
		for bgram in entities_bgrams:
			e1, e2 = bgram
			for rel in relations:
				if (e1[0] < rel[0]) and (rel[0] < e2[0]):
					triples.append((e1[1] + '/' + e1[2], e2[1] + '/' + e2[2], rel[1]))
		# print(e1, e2, rel)
	return triples


delimiter = '\t'

if __name__ == '__main__':
	input = "../tool/result.txt"
	output = "../tool/triples.txt"
	
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
	# print(len(sents))
	# for s in sents:
	# print(s)
	
	triples = extract_triples(sents)
	
	print("total triples:", len(triples))
	
	with open(output, 'w', encoding='utf-8') as f:
		for triple in triples:
			f.write(delimiter.join(triple))
			f.write("\n")
