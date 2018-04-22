#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:ner
   Author:jason
   date:18-4-22
-------------------------------------------------
   Change Activity:18-4-22:
-------------------------------------------------
"""

import os
from pyltp import NamedEntityRecognizer

LTP_DATA_DIR = "/home/jason/ltp_data"  # ltp模型目录的路径
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径

if __name__ == '__main__':
	input_words = "data/segments.txt"
	input_postags = "data/postaggs.txt"

	recognizer = NamedEntityRecognizer()  # 初始化实例
	recognizer.load(ner_model_path)  # 加载模型

	words = open(input_words, 'r').readlines()[0].strip().split()
	postags = open(input_postags, 'r').readlines()[0].strip().split()

	# words = ['元芳', '你', '怎么', '看']
	# postags = ['nh', 'r', 'r', 'v']

	netags = recognizer.recognize(words, postags)  # 命名实体识别

	print '\t'.join(words)
	print '\t'.join(netags)

	recognizer.release()  # 释放模型
