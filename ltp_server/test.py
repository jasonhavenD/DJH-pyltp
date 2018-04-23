#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:test
   Author:jason
   date:18-4-22
-------------------------------------------------
   Change Activity:18-4-22:
-------------------------------------------------
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib, urllib2
import json
uri_base = "http://127.0.0.1:12345/ltp"

data = {
    's': '我爱北京天安门',
    'x': 'n',
    't': 'all'}

request = urllib2.Request(uri_base)
params = urllib.urlencode(data)
response = urllib2.urlopen(request, params)
content = response.read().strip()
content=json.loads(content)

#segment
segmented_text_list = []
for text_other in content:
	sent = text_other[0]
	text = []
	for word in sent:
		text.append(word['cont'])
	segmented_text_list.append(text)
print(segmented_text_list)

#postag
postagger_text_list = []
for text_other in content:
	sent = text_other[0]
	text = []
	for word in sent:
		text.append([word['cont'], word['pos']])
	postagger_text_list.append(text)
print(postagger_text_list)


#ner
entity_text_list = []
Entity_dist=False
repead=False
for text_other in content:
	sent = text_other[0]
	text = []
	words_list = []
	entity_note_list = []
	for word in sent:
		text.append([word['cont'], word['ne']])
	entity_text_list.append(text)
print(entity_text_list)