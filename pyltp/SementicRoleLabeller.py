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
语义角色标注
'''

import os
from pyltp import SementicRoleLabeller
from pyltp import Parser

LTP_DATA_DIR = "/home/jason/ltp_data"  # ltp模型目录的路径
srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl.model')  # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`

if __name__ == '__main__':
	labeller = SementicRoleLabeller()  # 初始化实例
	labeller.load(srl_model_path)  # 加载模型
	parser = Parser()  # 初始化实例
	parser.load(par_model_path)  # 加载模型

	words = ['元芳', '你', '怎么', '看']
	postags = ['nh', 'r', 'r', 'v']

	arcs = parser.parse(words, postags)  # # arcs 使用依存句法分析的结果

	roles = labeller.label(words, postags, arcs)  # 语义角色标注

	'''
	返回结果 roles 是关于多个谓词的语义角色分析的结果。
	role.index 代表谓词的索引，
	role.arguments 代表关于该谓词的若干语义角色。
	arg.name 表示语义角色类型，
	arg.range.start 表示该语义角色起始词位置的索引，
	arg.range.end 表示该语义角色结束词位置的索引。
	'''

	# 打印结果
	for role in roles:
		print role.index, "".join(
			["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments])
	labeller.release()  # 释放模型
