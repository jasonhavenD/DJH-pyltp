#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:CustomizedSegmentor
   Author:jason
   date:18-4-22
-------------------------------------------------
   Change Activity:18-4-22:
-------------------------------------------------
"""

import os
from pyltp import CustomizedSegmentor

LTP_DATA_DIR = "/home/jason/ltp_data"  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`

if __name__ == '__main__':
	customized_segmentor = CustomizedSegmentor()  # 初始化实例
	# customized_segmentor.load(cws_model_path, '/path/to/your/customized_model')  # 加载模型，第二个参数是您的增量模型路径
	# customized_segmentor.load_with_lexicon(cws_model_path,'/path/to/your/customized_model', '/path/to/your/l, 'data/dict.txt')  # 加载模型,第3个参数是您的外部词典文件路径
	words = customized_segmentor.segment('亚硝酸盐是一种化学物质')
	print '\t'.join(words)
	customized_segmentor.release()
