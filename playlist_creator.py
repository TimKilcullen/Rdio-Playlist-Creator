
from __future__ import unicode_literals

import sys,os.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rdio import Rdio
#python file with your developer rdio credentials
from rdio_consumer_credentials import RDIO_CREDENTIALS
import urllib2
import json
import webbrowser

try:
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError
from bs4 import BeautifulSoup


# create an instance of the Rdio object with our consumer credentials
rdio = Rdio(RDIO_CREDENTIALS)

#have to get the key for each track in your file
def get_keys():
	# Fix for Python 2.X
	try:
		input = raw_input
	except NameError:
		pass
	try:
		# authenticate against the Rdio service
		url = rdio.begin_authentication('oob')
		print('Go to: ' + url)
		#open url
		webbrowser.open(url)
		verifier = input('\nThen enter the code: ').strip()
		rdio.complete_authentication(verifier)


		#open file of songs/artists, enter your filename...
		f = open("yourfilename.txt","r")
		lines = f.readlines()

		print 'getting keys...'
		keys = []
		not_found = []
		#create new files to store keys and songs not found
		key_file = open('key_file.txt','w')
		missing_file = open('missing_key_file.txt','w')

		for line in lines:
			
			#query rdio using the artist and song. only get the first track from the result
			param = {
			  'query' : line,
			  'types' : 'Tracks',
			  'count' : '1'
			  }
			#get key from rdio search query
			results = rdio.call('search',param)['result']['results']
			if len(results) >= 1:
				result = results[0]
				if 'key' in result:
					key = result['key']
					print key
					keys.append(key)
					key_file.write(key+'\n')
			else:
				print 'Not found: '+line
				not_found.append(line)
				missing_file.write(line+'\n')
		print 'done.'
		#print all keys not found to the console
		print 'keys not found:\n'
		for song in not_found:
			print song
		#close files
		key_file.close()
		missing_file.close()
		return keys
	except HTTPError as e:
		# if we have a protocol error, print it
		print(e.read())

#uses the keys file to 
def create_playlist(keys):
	try:
		#get comma separated string from list of keys
		key_string = ','.join(keys)
		#create a new playlist with the keys
		param = {
			'name':'My Playlist',
			'description' :'',
			'tracks': key_string
		}
		print 'creating playlist...'
		#send the request
		playlist = rdio.call('createPlaylist',param)
		print playlist
	except HTTPError as e:
		# if we have a protocol error, print it
		print(e.read())


keys = get_keys()
create_playlist(keys)