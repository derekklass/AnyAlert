# import modules
import pyrebase
import spotipy
import time
import re

# needed for Spotify authentication
from spotipy.oauth2 import SpotifyOAuth
from spotipy import util


# initialize needed global objects
album_dict = {}
artist_list = []
raw_data = []

print('testing1')
# authenticate with firebase
def firebase_authentication():
	config = {
	'apiKey': '',
	'authDomain': 'anyalert.firebaseapp.com',
	'databaseURL': 'https://anyalert-default-rtdb.firebaseio.com/',
	'storageBucket': 'anyalert.appspot.com'
	}

	global db
	firebase = pyrebase.initialize_app(config)
	db = firebase.database()

firebase_authentication()
print('testing2')

# download artist_list and album_dict from firebase
def firebase_download():
	global artist_list
	artist_list = list(db.child('notifications').child('spotify').child('artist').get().val().keys())

	try:
		for artist in artist_list:
			album_dict[artist] = list(db.child('storage').child('spotify').child('artist').child(artist).get().val().keys())
	except:
		pass

firebase_download()
print('testing3')

# listen for changes in database and redownload artist_list
def stream_handler(message):
	global artist_list
	artist_list = list(db.child('notifications').child('spotify').child('artist').get().val().keys())
	print('testingerr')

stream_firebase_notification_changes = db.child('notifications').child('spotify').child('artist').stream(stream_handler)
print('testing4')

def spotify_authentication():
	print('testing51')
	# authenticate with spotify
	token = util.prompt_for_user_token(scope = 'user-library-read',
									client_id = 'f32ebfa449e04779a05c6e752f25f1a4',
									client_secret = '',
									redirect_uri = 'http://localhost:8000',
									cache_path = 'cache//cache_file.cache')

	print('testing52')
	global sp
	sp = spotipy.Spotify(auth=token)
	print('testing53')

spotify_authentication()
print('testing59')

# check artists' album data and compare to previous album data every specified unit of time
def album_comparison_loop():
	global artist_list

	while True:
		for item in artist_list:

			# find artist
			results = sp.search(q='artist:' + item, type='artist')
			items = results['artists']['items']
			try:
				artist = items[0]
			except:
				print('Artist: ' + item + ' not found in Spotify.')
				continue

			print('testing10')
			# get artist's album data
			album_data = []
			results = sp.artist_albums(artist['id'], album_type='album')
			album_data.extend(results['items'])
			while results['next']:
				results = sp.next(results)
				album_data.extend(results['items'])

			# parse the spotify album data into an album list
			albums = []
			album_data.sort(key=lambda album: album['name'].lower())
			for album in album_data:
				name = album['name']
				if name not in albums:
					albums.append(name)

			# notify new album if there is something new in the artist's album list
			try:
				if albums.sort() != album_dict[item].sort():
					new_album = set(albums) - set(album_dict[item])
					notification_info = [item, new_album]
					print(notification_info)

					album_dict[item] = albums

					# parse out characters that can't be uploaded to firebase
					for album in albums:
						albums[albums.index(album)] = re.sub('[^0-9a-zA-Z]+', ' ', album)

					# update firebase with new album
					for album in albums:
						try:
							db.child('storage').child('spotify').child('artist').child(item).update({album: '0'})

						except:
							db.update({'storage/spotify/artist/' + item: {album: '0'}})

			# if artist was never detected before, add their album list to the dictionary
			except:
				album_dict[item] = albums

				# parse out characters that can't be uploaded to firebase
				for album in albums:
					albums[albums.index(album)] = re.sub('[^0-9a-zA-Z]+', ' ', album)

				for album in albums:
					try:
						db.child('storage').child('spotify').child('artist').child(item).update({album: '0'})

					except:
						db.update({'storage/spotify/artist/' + item: {album: '0'}})

		time.sleep(1) # how often should the loop check the artists' pages


album_comparison_loop()
