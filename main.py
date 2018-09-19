# How to get an API key? http://www.omdbapi.com/apikey.aspx
# Get reviews from an API? https://developers.themoviedb.org/3/reviews/get-review-details
# Dataset : http://ai.stanford.edu/%7Eamaas/data/sentiment/
# To start, just download the dataset, and extract the file in the same folder of the main.py

import omdb
import json
import os

#debug print and return the movie info
def get_imdb_info(id, type='movie'):
	API_KEY = "68735ac"

	omdb.set_default('apikey', API_KEY)
	omdb.set_default('tomatoes', True)

	movie = omdb.imdbid(id, fullplot=True, tomatoes=True)

	url = 'https://www.imdb.com/title/' + movie['imdb_id'] + '/'
	print (url)
	print (json.dumps(movie, indent=4, sort_keys=True))
	#return and info about the movie
	return movie

#get the files from a directory structure
def get_files_name(pattern='train'):
	files_name = []

	for dirname, dirnames, filenames in os.walk('.'):

		# print path to all subdirectories first.
		for subdirname in dirnames:
			print(os.path.join(dirname, subdirname))
		
		#garantees the pattern in the name and get only usefull data
		if pattern in dirname and len(dirnames) == 0:
			# print path to all filenames.
			for filename in filenames:
				files_name.append(filename)
				#print(os.path.join(dirname, filename))

		# Advanced usage:
		# editing the 'dirnames' list will stop os.walk() from recursing into there.
		if '.git' in dirnames:
		# don't go into any .git directories.
			dirnames.remove('.git')

	return files_name

get_imdb_info('tt0010790')
files_name = get_files_name('train')
