#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:segmentor
   Author:jason
   date:18-4-22
-------------------------------------------------
   Change Activity:18-4-22:
-------------------------------------------------
"""

import os
from pyltp import Segmentor

LTP_DATA_DIR = "/home/jason/ltp_data"  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`


def use_other_lexicon():
	input_lexicon = 'lexicon/word.txt'
	segmentor = Segmentor()  # 初始化实例
	segmentor.load_with_lexicon(cws_model_path, input_lexicon)  # 加载模型，第二个参数是您的外部词典文件路径
	words = segmentor.segment('亚硝酸盐是一种化学物质')
	print '\t'.join(words)
	segmentor.release()


if __name__ == '__main__':
	input = "data/sentcences.txt"
	output = "data/segments.txt"

	use_other_lexicon()

	print "loading Segmentor......"
	segmentor = Segmentor()  # 初始化实例
	segmentor.load(cws_model_path)  # 加载模型

	print "model has been loaded......"

	sents = []
	with open(input, 'r') as f:
		sents = f.readlines()

	with open(output, 'w') as f:
		for sent in sents:
			if sent.strip() == '':
				continue
			words = segmentor.segment(sent)
			f.write('\t'.join(words))
			f.write('\n')

	segmentor.release()  # 释放模型
	print "model has been released......"
