# import modules
import pyrebase
import spotipy
import time
import subprocess

# needed for Spotify authentication
from spotipy.oauth2 import SpotifyOAuth
from spotipy import util

config = {
  "apiKey": "",
  "authDomain": "anyalert.firebaseapp.com",
  "databaseURL": "https://anyalert-default-rtdb.firebaseio.com/",
  "storageBucket": "anyalert.appspot.com"
}


firebase = pyrebase.initialize_app(config)
db = firebase.database()

#db.child("users").child("000000001").update({"000000001update0": "Minecraft!"})

#print(db.child("notifications").child("spotify").child("artist").child('Travis Scott').get().val())
'''
info = 'Travis Scott'
id = '000000003'

if info not in db.child("notifications").child("spotify").child("artist").get().val():
  data = {"notifications/spotify/artist/" + info: {id: 'exampletoken'}}
  db.update(data)

else:
  data = {id: '1'}
  db.child("notifications").child("spotify").child("artist").child(info).update(data)
  '''

#db.child("storage").child("spotify").child("artist").child("Drake").update({'sup fellers': '0'})

'''
def spotify_authentication():
	# authenticate with spotify
	token = util.prompt_for_user_token(scope = 'user-library-read',
									client_id = 'f32ebfa449e04779a05c6e752f25f1a4',
									client_secret = '',
									redirect_uri = 'http://localhost:8000')

	global sp
	sp = spotipy.Spotify(auth=token)

spotify_authentication()



pl_id = 'spotify:playlist:5XIvQAvtOsQaSu81DasXXs'
offset = 0

# first run through also retrieves total no of songs in library
response = sp.playlist_items(pl_id,
                                 offset=offset,
                                 fields='items.track.id,total',
                                 additional_types=['track'])
results = response["items"]

# subsequently runs until it hits the user-defined limit or has read all songs in the library
while len(results) < response["total"]:
	response = sp.playlist_items(pl_id,
                                 offset=offset,
                                 fields='items.track.id,total',
                                 additional_types=['track'])
	results.extend(response["items"])

playlist_track_ids = []

for item in results:
	playlist_track_ids.append(list(list(item.values())[0].values())[0])

#print(sp.track('5bgwqaRSS3M8WHWruHgSL5'))


print(sp.current_user_playlists()) # spotipy can't get user's followed playlists, can only check if they follow a certain playlist or not, so either set up a pre determined amount of popular playlists in the app to choose from or allow the user to search for playlists
'''
import os # Ubuntu
os.system('cd/ whatever')
os.system('xdg-open spotify_loop.py')



















'''




  # import modules
import spotipy

# needed for Spotify authentication
from spotipy.oauth2 import SpotifyOAuth
from spotipy import util


# authenticate user
token = util.prompt_for_user_token(scope = 'user-library-read',
                                   client_id = 'f32ebfa449e04779a05c6e752f25f1a4',
                                   client_secret = '924c8f58f0cc44608ee33c26d68b3fbd',
                                   redirect_uri = 'http://localhost:8000')

sp = spotipy.Spotify(auth=token)


# download every artist in current user's liked songs
artists = []

def show_tracks(results):
    for item in results['items']:
        track = item['track']
        artists.append(track['artists'][0]['name'])

results = sp.current_user_saved_tracks()
show_tracks(results)

while results['next']:
    results = sp.next(results)
    show_tracks(results)

print(artists)


# download every album from a particular artist
artist_name = 'Travis Scott'
results = sp.search(q='artist:' + artist_name, type='artist')
items = results['artists']['items']
artist = items[0]

albumdata = []
results = sp.artist_albums(artist['id'], album_type='album')
albumdata.extend(results['items'])
while results['next']:
    results = sp.next(results)
    albumdata.extend(results['items'])

albums =[]
albumdata.sort(key=lambda album: album['name'].lower())
for album in albumdata:
    name = album['name']
    if name not in albums:
        albums.append(name)

print(albums)

'''
