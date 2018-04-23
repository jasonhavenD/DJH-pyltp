#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:Parser
   Author:jason
   date:18-4-22
-------------------------------------------------
   Change Activity:18-4-22:
-------------------------------------------------

"""


'''
依存句法分析
'''

import os

LTP_DATA_DIR = "/home/jason/ltp_data"  # ltp模型目录的路径
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`

from pyltp import Parser

if __name__ == '__main__':
	parser = Parser()  # 初始化实例
	parser.load(par_model_path)  # 加载模型

	words = ['元芳', '你', '怎么', '看']
	postags = ['nh', 'r', 'r', 'v']
	arcs = parser.parse(words, postags)  # 句法分析

	print "\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)
	parser.release()  # 释放模型