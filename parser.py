import os
import nltk
import random		

from review import Review
from collections import Counter, OrderedDict
from sklearn.feature_extraction import DictVectorizer

class Parser:
	pattern = ''
	files = []
	
	def __init__(self, pattern):
		self.n = 1
		self.pattern = pattern
		self.files = []

	#get the files from a directory structure
	def get_files_name(self):

		for dirname, dirnames, filenames in os.walk('.'):

			# print path to all subdirectories first.
			for subdirname in dirnames:
				print(os.path.join(dirname, subdirname))
			
			#garantees the pattern in the name and get only usefull data
			if self.pattern in dirname and len(dirnames) == 0:
				# print path to all filenames.
				for filename in filenames:
					self.files.append([dirname, filename])
					#print(os.path.join(dirname, filename))

			# Advanced usage:
			# editing the 'dirnames' list will stop os.walk() from recursing into there.
			if '.git' in dirnames:
			# don't go into any .git directories.
				dirnames.remove('.git')

		return self.files

	def make_bag_of_words(self, ngram_count, reviews, threshold, n=1):
		bag_of_words = []
		self.ngram_idx = {}
		filtered_list = []
		self.sorted_ngrams = []
		rating_list = []
		j = 0

		for key,val in ngram_count.items():
			if(val > threshold):
				self.sorted_ngrams.append(key)
		
		self.sorted_ngrams.sort()
		print (len(self.sorted_ngrams))
		
		for ngram in self.sorted_ngrams:
			self.ngram_idx[ngram] = j
			j += 1

		for i in range(len(reviews)):
			tmp = self.bag_of_one_word(reviews[i], n)
			bag_of_words.append(tmp)
			if(reviews[i].rating <= 3):
				rating_list.append([1, 0, 0])
			elif(reviews[i].rating >= 4 and reviews[i].rating <= 6):
				rating_list.append([0, 1, 0])
			else:
				rating_list.append([0, 0, 1])

		return bag_of_words, rating_list, len(self.sorted_ngrams)

	def bag_of_one_word(self, review, n=1):
		if(n > 1):
			review_ngrams = review.generate_ngrams(n=n)
		else:
			review_ngrams = review.review
		tmp = [0] * (len(self.ngram_idx))

		for ngram in review_ngrams:
			if(ngram in self.ngram_idx):
				idx = self.ngram_idx[ngram]
				tmp[idx] += 1

		return tmp			

	def get_data_from_file(self):
		ngram_count = {}
		ngrams_list = []
		reviews = []
		x_train_dataset = []
		y_train_dataset = []
		threshold = 128
		
		train = random.sample(self.files, 10000)
		#train = self.files

		for path in train:
			if('train' not in path[0]):
				continue

			with open(path[0] + '/' + path[1]) as reader:
				review = reader.read()
				review = Review(review, path)
				if(self.n > 1):
					ngrams = review.generate_ngrams(n=2)
				else:
					ngrams = review.review
				
				reviews.append(review)
				
				for elem in ngrams:
					if(elem not in ngram_count):
						ngram_count[elem] = 0
					ngram_count[elem] += 1

		x_train_dataset, y_train_dataset, input_size = self.make_bag_of_words(ngram_count, reviews, threshold)		
		
		return x_train_dataset, y_train_dataset, reviews, input_size