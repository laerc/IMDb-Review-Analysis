import re

from sets import Set
from nltk.stem.porter import PorterStemmer

porter_stemmer = PorterStemmer()

class Analyser:
	tags = {}
	score = {}
	adj_idx = {}
	adj_list = []

	def __init__(self):
		self.tags['JJ'] = 'a'
		self.tags['JJR'] = 'a'
		self.tags['JJS'] = 'a'
		self.tags['NN'] = 'n'
		self.tags['NNP'] = 'n'
		self.tags['NNPS'] = 'n'
		self.tags['NNS'] = 'n'
		self.tags['RB'] = 'r'
		self.tags['RBR'] = 'r'
		self.tags['RBS'] = 'r'
		self.tags['RP'] = 'r'
		self.tags['VB'] = 'v'
		self.tags['VBD'] = 'v'
		self.tags['VBG'] = 'v'
		self.tags['VBN'] = 'v'
		self.tags['VBP'] = 'v'
		self.tags['VBZ'] = 'v'
		self.adjectives_tags = Set(['JJ', 'JJR', 'JJS'])

	def get_tag(self, word_type):
		if(word_type in self.tags):
			return self.tags[word_type]
		else:
			return None

	def get_score_from_file(self):
		lines = []
		count = 0
		with open('SentiWords_1.1.txt') as reader:
			lines = reader.readlines()
		for line in lines:
			splt_line = re.split('[# |\t|\n]',line)
			self.score[(porter_stemmer.stem(splt_line[0]), splt_line[1])] = float(splt_line[2])
			if(splt_line[1] == 'a'):
				self.adj_list.append(porter_stemmer.stem(splt_line[0]))
			if(float(splt_line[2]) != 0):
				count+=1

		for i in range(len(self.adj_list)):
			self.adj_idx[self.adj_list[i]] = i

	def get_word_score(self, word, word_type):
		
		if(word_type in self.tags):
			word_type = self.tags[word_type]
		else:
			return 0

		if((word, word_type) in self.score):
			return self.score[(word, word_type)]
		else:
			return 0.0

	def isAdjective(self, word_type):
		return word_type in self.adjectives_tags

	def generate_input_score(self, review_scores):
		score_input = len(self.adj_list) * [0]
		for key, val in review_scores.items():
			if(key not in self.adj_list):
				continue
			idx = self.adj_idx[key]
			score_input[idx] = val
		return score_input
 