# How to get an API key? http://www.omdbapi.com/apikey.aspx
# Get reviews from an API? https://developers.themoviedb.org/3/reviews/get-review-details
# Dataset : http://ai.stanford.edu/%7Eamaas/data/sentiment/
# To start, just download the dataset, and extract the file in the same folder of the main.py

import os
import re
import json
import omdb
import bs4
import nltk

ID_SIZE = 7

def format_id(id):
	if 'tt' not in id:
		id = 'tt' + ('0' * (ID_SIZE - len(id)) + id)

	return id

def clean_string(review):
	text = bs4.BeautifulSoup(review, "lxml")
	return text.get_text()

#debug print and return the movie info
def get_imdb_info(id, type='movie'):
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

#get the files from a directory structure
def get_files_name(pattern='train'):
	filenames_ret = []

	for dirname, dirnames, filenames in os.walk('.'):

		# print path to all subdirectories first.
		for subdirname in dirnames:
			print(os.path.join(dirname, subdirname))
		
		#garantees the pattern in the name and get only usefull data
		if pattern in dirname and len(dirnames) == 0:
			# print path to all filenames.
			for filename in filenames:
				filenames_ret.append([dirname, filename])
				#print(os.path.join(dirname, filename))

		# Advanced usage:
		# editing the 'dirnames' list will stop os.walk() from recursing into there.
		if '.git' in dirnames:
		# don't go into any .git directories.
			dirnames.remove('.git')

	return filenames_ret

def parse_data(review, path_to_file):
	
	parsed_string = re.split('[_ |.]',path_to_file[1])
	
	id, rating = format_id(parsed_string[0]), int(parsed_string[1])
	review = clean_string(review)
	print (id, rating)

	return {'id': id, 'rating': rating, 'review': review}

def get_data_from_file(filenames = []):
	reviews = []

	for path in filenames:
		with open(path[0] + '/' + path[1]) as reader:
			review = reader.read()
			reviews.append(parse_data(review, path))
	
	return reviews


get_imdb_info('10790')
files_name = get_files_name('train')
get_data_from_file(files_name)