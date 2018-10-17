import re
import bs4
import nltk
import omdb

from analyser import Analyser
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

porter_stemmer = PorterStemmer()

analyser = Analyser()
analyser.get_score_from_file()

_stopwords = stopwords.words("english")
_stopwords.remove('very')

#Class that holds information about the each review
class Review:
	ID_SIZE = 7
	path_to_file = ''	
	review = []
	tokens = []

	pos_score_review = 0.0
	neg_score_review = 0.0
	adjective_score = {}

	def __init__(self, review, path = None):
		# A set of words that contain default stop words in english
		self.sw = _stopwords

		#remove words that may contains information about negative reviews
		#self.sw.remove('not')
		#print (self.sw)
		
		self.id = None
		self.rating = None
		self.review = review
		self.path_to_file = path
		
		if(path != None):
			self.parse_data()

		self.clean_string()

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

	def parse_data(self):
		#print(path_to_file)
		self.parsed_string = re.split('[_ |.]',self.path_to_file[1])
		self.id, self.rating = self.format_id(self.parsed_string[0]), int(self.parsed_string[1])
		#print (self.id, self.rating)

	def clean_string(self):
		#remove all the html tags
		self.review = self.remove_html_tags()
		#tokenize the words and remove all the non alpha characters
		self.review = self.tokenize_string()

		#remove stop words
		self.review = self.remove_stop_words()

	def remove_stop_words(self):
		return [word for word in self.review if word not in self.sw]

	def get_score(self, n_gram=1, phrase_form=['a']):
		
		#nltk.help.upenn_tagset()
		word_types = nltk.pos_tag(self.review)
		self.generate_ngrams(n=n_gram)

		for i in range(len(self.review)- n_gram + 1):	
			tmp = []
			words = []
			for j in range(i,i+n_gram):
				word = self.review[j]
				word_type = word_types[j][1]
				score = analyser.get_word_score(porter_stemmer.stem(word), word_type)
				if (phrase_form[j-i] == 'any' or phrase_form[j-i] == analyser.get_tag(word_type)):
					tmp.append((word, word_type, score))
					words.append(word)
				else:
					tmp = []
					break
			if(len(tmp) != 0):
				word = self.review[i+1]
				score = tmp[0][-1] * tmp[1][-1]

				if(word not in self.adjective_score):
					self.adjective_score[word] = 0.

				self.adjective_score[word] += (score)
				
				if(score >= 0):
					self.pos_score_review += score
				else:
					self.neg_score_review -= score

	def get_sign(self, score):
		if(score >= 0):
			return 1
		else:
			return -1

	# This method apply tokenize to the string
	def tokenize_string(self):
		# tokenize the string
		self.tokens = nltk.word_tokenize(self.review)
		self.tokens = [word.lower() for word in self.tokens if word.isalpha()]
		return self.tokens

	def generate_ngrams(self, n=1):
		ngrams = nltk.ngrams(self.review,n)
		ngrams = [ngram for ngram in ngrams]
		return ngrams
