#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:SentenceSplitter
   Author:jason
   date:18-4-22
-------------------------------------------------
   Change Activity:18-4-22:
-------------------------------------------------
"""

MODELDIR = "/home/jason/ltp_data"

import sys
import os

from pyltp import SentenceSplitter

if __name__ == '__main__':
	input = "data/raw.txt"
	output = "data/sentcences.txt"

	text = ""
	with open(input, 'r') as fin:
		text = fin.read()

	with open(output, 'w') as fout:
		sents = SentenceSplitter.split(text)
		fout.writelines('\n'.join(sents))
