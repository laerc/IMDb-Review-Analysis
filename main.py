# How to get an API key? http://www.omdbapi.com/apikey.aspx
# Get reviews from an API? https://developers.themoviedb.org/3/reviews/get-review-details
# Dataset : http://ai.stanford.edu/%7Eamaas/data/sentiment/
# To start, just download the dataset, and extract the file in the same folder of the main.py

import os
import re
import bs4
import json
import nltk
import omdb

from nltk.corpus import stopwords

#Class that holds information about the each review
class Review:
	ID_SIZE = 7
	path_to_file = ''	
	review = []

	# A set of words that contain default stop words in english

	def __init__(self, review, path):
		self.sw = stopwords.words("english")

		#remove words that may contains information about negative reviews
		self.sw.remove('not')
		self.sw.remove('very')
		print (self.sw)
		
		self.review = review
		self.path_to_file = path
		self.parse_data(self.review, self.path_to_file, self.sw)

	def format_id(self, id):
		if 'tt' not in id:
			id = 'tt' + ('0' * (self.ID_SIZE - len(id)) + id)

		return id

	def remove_html_tags(self):
		text = bs4.BeautifulSoup(self.review, "lxml")
		return text.get_text()

	#debug print and return the movie info
	def get_imdsb_info(self, id, type='movie'):
		API_KEY = "68735ac"

		omdb.set_default('apikey', API_KEY)
		omdb.set_default('tomatoes', True)

		id = format_id(id)
		movie = omdb.imdbid(id, fullplot=True, tomatoes=True)

		url = 'https://www.imdb.com/title/' + movie['imdb_id'] + '/'
		print (url)
		print (json.dumps(movie, indent=4, sort_keys=True))
		#return and info about the movie
		return movie

	def parse_data(self, review, path_to_file, sw):
		print(path_to_file)
		parsed_string = re.split('[_ |.]',self.path_to_file[1])
		
		id, rating = self.format_id(parsed_string[0]), int(parsed_string[1])
		#remove all the html tags
		self.review = self.remove_html_tags()
		#tokenize the words and remove all the non alpha characters
		self.review = self.tokenize_string()

		#remove stop words
		self.review = self.remove_stop_words()
		
		print (id, rating)

		return {'id': id, 'rating': rating, 'review': review}

	def remove_stop_words(self):
		return [word for word in self.review if word not in self.sw]

	# This method apply tokenize to the string
	def tokenize_string(self):
		# tokenize the string
		tokens = nltk.word_tokenize(self.review)
		tokens = [word.lower() for word in tokens if word.isalpha()]
		return tokens

	def generate_ngrams(self, n=1):
		ngrams = nltk.ngrams(self.review,n)
		return ngrams

class Parser:
	pattern = ''
	files = []
	
	def __init__(self, pattern):
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

	def get_data_from_file(self):
		reviews = []
		j = 0
		for path in self.files:
			with open(path[0] + '/' + path[1]) as reader:
				review = reader.read()
				review = Review(review, path)
				ngrams = review.generate_ngrams(n=3)
				reviews.append(review)
		return reviews

def start():
	nltk.download('punkt')
	nltk.download('stopwords')

start()
parser = Parser('train')
filenames = parser.get_files_name()
parser.get_data_from_file()