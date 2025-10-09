#!env python
# Simple indexer by Adewale Oshineye
#3-9-2001

usage="""
Usage: myIndexer.py fileToBeIndexed

"""
__author__  = "Adewale Oshineye"

def readWord(file):
	word = ""
	while(1):#loop forever
		c = file.read(1)#read a char at a time
		if c == ' ' or c == '\t' or c == '\n' or c == '\r':
			return word
		if c == '':#return a special value to indicate EndOfFile
			print "EOF"
			return None
		word += c
	

def getIndex(file):
	dict = {}
	
	while(1):
		word = readWord(file)
		if word==None:
			print "File finished"
			break;

		#print "the word is:: ",word

		if dict.has_key(word):
			dict[word] += 1
		else:
			dict[word] = 1
	return dict

def printIndex(indexToPrint):
	keys = indexToPrint.keys()
	keys.sort()
	for key in keys:
		print key, " : ", indexToPrint[key]
	

import sys
fileToIndex = sys.argv[1]

if __name__=='__main__':
	dict_index = getIndex(open(fileToIndex, 'r'))
	printIndex(dict_index)