#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:re
   Author:jason
   date:18-4-23
-------------------------------------------------
   Change Activity:18-4-23:
-------------------------------------------------
"""
import os
import codecs

from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer


def triple_extract(sentence):
	words = segmentor.segment(sentence)
	postags = postagger.postag(words)
	netags = recognizer.recognize(words, postags)
	arcs = parser.parse(words, postags)
	child_dict_list = build_parse_child_dict(words, postags, arcs)

	triples = []
	for index in range(len(postags)):
		# 抽取以谓词为中心的三元组
		if postags[index] == 'v':
			child_dict = child_dict_list[index]
			# 主谓宾
			if child_dict.has_key('SBV') and child_dict.has_key('VOB'):
				e1 = complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
				r = words[index]
				e2 = complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
				triples.append("主语谓语宾语关系\t({},{},{})".format(e1, r, e2))
			# 定语后置，动宾关系
			if arcs[index].relation == 'ATT':
				if child_dict.has_key('VOB'):
					e1 = complete_e(words, postags, child_dict_list, arcs[index].head - 1)
					r = words[index]
					e2 = (words, postags, child_dict_list, child_dict['VOB'][0])
					temp_string = r + e2
					if temp_string == e1[:len(temp_string)]:
						e1 = e1[len(temp_string):]
					if temp_string not in e1:
						triples.append("定语后置动宾关系\t({},{},{})".format(e1, r, e2))
			# 含有介宾关系的主谓动补关系
			if child_dict.has_key('SBV') and child_dict.has_key('CMP'):
				# e1 = words[child_dict['SBV'][0]]
				e1 = complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
				cmp_index = child_dict['CMP'][0]
				r = words[index] + words[cmp_index]
				if child_dict_list[cmp_index].has_key('POB'):
					e2 = complete_e(words, postags, child_dict_list, child_dict_list[cmp_index]['POB'][0])
					triples.append("介宾关系主谓动补\t({},{},{})".format(e1, r, e2))

		# 尝试抽取命名实体有关的三元组
		if netags[index][0] == 'S' or netags[index][0] == 'B':
			ni = index
			if netags[ni][0] == 'B':
				while netags[ni][0] != 'E':
					ni += 1
				e1 = ''.join(words[index:ni + 1])
			else:
				e1 = words[ni]
			if arcs[ni].relation == 'ATT' and postags[arcs[ni].head - 1] == 'n' and netags[arcs[ni].head - 1] == 'O':
				r = complete_e(words, postags, child_dict_list, arcs[ni].head - 1)
				if e1 in r:
					r = r[(r.index(e1) + len(e1)):]
				if arcs[arcs[ni].head - 1].relation == 'ATT' and netags[arcs[arcs[ni].head - 1].head - 1] != 'O':
					e2 = complete_e(words, postags, child_dict_list, arcs[arcs[ni].head - 1].head - 1)
					mi = arcs[arcs[ni].head - 1].head - 1
					li = mi
					if netags[mi][0] == 'B':
						while netags[mi][0] != 'E':
							mi += 1
						e = ''.join(words[li + 1:mi + 1])
						e2 += e
					if r in e2:
						e2 = e2[(e2.index(r) + len(r)):]
					if r + e2 in sentence:
						triples.append("机构//地名//人名\t({},{},{})".format(e1, r, e2))
	return triples


def extract_from_file(fin_name, fout_name):
	sents = []
	with codecs.open(fin_name, 'r')as fin:
		sents = fin.readlines()

	with codecs.open(fout_name, 'a')as fout:
		for sent in sents:
			if sent == "" or len(sent) > 1000:
				continue
			try:
				triples = triple_extract(sent.strip())
				if triples == []:
					continue
				fout.write('\n'.join(triples))
				fout.write('\n')
			except Exception as e:
				pass


def extract_from_sents(sents):
	for sent in sents:
		try:
			triples = triple_extract(sent.strip())
			if triples == []:
				continue
			print(sent)
			print('\n'.join(triples))
		except Exception as e:
			pass


def build_parse_child_dict(words, postags, arcs):
	'''
	为句子中的每个词语维护一个保存句法依存儿子节点的字典
	:param words: 分词列表
	:param postags: 词性列表
	:param arcs:句法依存列表
	:return:字典
	'''
	child_dict_list = []
	for index in range(len(words)):
		child_dict = dict()
		for arc_index in range(len(arcs)):
			if arcs[arc_index].head == index + 1:
				if child_dict.has_key(arcs[arc_index].relation):
					child_dict[arcs[arc_index].relation].append(arc_index)
				else:
					child_dict[arcs[arc_index].relation] = []
					child_dict[arcs[arc_index].relation].append(arc_index)
		child_dict_list.append(child_dict)
	return child_dict_list


def complete_e(words, postags, child_dict_list, word_index):
	'''
	完善识别的部分实体
	:param words:分词列表
	:param postags:词性列表
	:param child_dict_list:句法依存节点的字典
	:param word_index:location
	:return:entity
	'''
	child_dict = child_dict_list[word_index]
	prefix = ''
	if child_dict.has_key('ATT'):
		for i in range(len(child_dict['ATT'])):
			prefix += complete_e(words, postags, child_dict_list, child_dict['ATT'][i])

	postfix = ''
	if postags[word_index] == 'v':
		if child_dict.has_key('VOB'):
			postfix += complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
		if child_dict.has_key('SBV'):
			prefix = complete_e(words, postags, child_dict_list, child_dict['SBV'][0]) + prefix

	return prefix + words[word_index] + postfix


LTP_DATA_DIR = "/home/jason/ltp_data"  # ltp模型目录的路径

if __name__ == "__main__":
	cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
	pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
	par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')
	ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')
	print("loading models......")
	segmentor = Segmentor()
	segmentor.load(cws_model_path)
	print("{} has been loaded......".format('cws.model'))

	postagger = Postagger()
	postagger.load(pos_model_path)
	print("{} has been loaded......".format('pos.model'))

	parser = Parser()
	parser.load(par_model_path)
	print("{} has been loaded......".format('parser.model'))

	recognizer = NamedEntityRecognizer()
	recognizer.load(ner_model_path)
	print("{} has been loaded......".format('ner.model'))
	input_sents = "data/sentcences.txt"
	output_triples = "data/triples.txt"

	# extract_from_file(input_sents, output_triples)
	sents = ['星展集团是亚洲最大的金融服务集团之一, 拥有约3千5百亿美元资产和超过280间分行, 业务遍及18个市场',
	         '6岁时，奥巴马随母亲和继父前往印度尼西亚首都雅加达生活，并在当地的一所小学就读了两年。']
	extract_from_sents(sents)
	print("release models......")
	segmentor.release()
	postagger.release()
	parser.release()
	recognizer.release()
