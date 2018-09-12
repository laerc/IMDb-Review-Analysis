# How to get an API key? http://www.omdbapi.com/apikey.aspx

import omdb
import json

import requests
import bs4

API_KEY = "68735ac"

omdb.set_default('apikey', API_KEY)
omdb.set_default('tomatoes', True)

tv_show_name = "deadpool 2"

movie = omdb.get(title=tv_show_name, fullplot=True, media_type="movie")

url = 'https://www.imdb.com/title/' + movie['imdb_id'] + '/'
print (url)

'''
source_code = requests.get(url)
plain_text = source_code.text
soup = bs4.BeautifulSoup(plain_text, 'html.parser')
print (soup)
'''

print (json.dumps(movie, indent=4, sort_keys=True))