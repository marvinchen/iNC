# -*- coding: utf-8 -*-
import jieba
import jieba.posseg as pseg
import os
import sys
import sklearn
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

if __name__=='__main__':
	with open('tf_test-Utf-8.txt', encoding="utf-8") as f:
		cor = f.readlines()
	strRes = ''
	first = True
	for c in cor:
		words = pseg.cut(c)
		for key in words:
			#print(str(key).split('/')[0])
			if first:
				strRes = str(key).split('/')[0]
				first = False
			else:
				strRes = strRes + str(key).split('/')[0] + ' '
	corpus = strRes.strip().split('\n ')

	vectorizer=CountVectorizer()
	transformer=TfidfTransformer()
	tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))
	word=vectorizer.get_feature_names()
	weight=tfidf.toarray()  
	for i in range(len(weight)): 
	    print ('Line No.', i)
	    for j in range(len(word)):
	        print (word[j],weight[i][j])
