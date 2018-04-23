#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:Postagger
   Author:jason
   date:18-4-22
-------------------------------------------------
   Change Activity:18-4-22:
-------------------------------------------------
"""

import os
from pyltp import Postagger

LTP_DATA_DIR = "/home/jason/ltp_data"  # ltp模型目录的路径
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')


def use_other_lexicon():
	input_lexicon='lexicon/postag.txt'
	postagger = Postagger()  # 初始化实例
	postagger.load_with_lexicon(pos_model_path,input_lexicon)
	words = ['元芳', '你', '怎么', '看']
	postags = postagger.postag(words)
	print('\t'.join(postags))
	postagger.release()  # 释放模型


if __name__ == '__main__':
	input = "data/segments.txt"
	output = "data/postaggs.txt"
	# use_other_lexicon()
	#
	print "loading Segmentor......"
	postagger = Postagger()  # 初始化实例
	postagger.load(pos_model_path)
	print "model has been loaded......"

	wordses = []
	with open(input, 'r') as f:
		wordses = f.readlines()

	with open(output, 'w') as f:
		for words in wordses:
			postags = postagger.postag(words.strip().split())  # 词性标注
			f.write('\t'.join(postags))
			f.write('\n')
	postagger.release()  # 释放模型
