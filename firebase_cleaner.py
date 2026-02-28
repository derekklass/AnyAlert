# import modules
import pyrebase


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


# download artist_list and album_dict from firebase
def firebase_download():
	global artist_list
	artist_list = list(db.child('notifications').child('spotify').child('artist').get().val().keys())

firebase_download()


# listen for changes in database and redownload artist_list
def stream_handler(message):
	global artist_list
	artist_list = list(db.child('notifications').child('spotify').child('artist').get().val().keys())
	storage_list = list(db.child('storage').child('spotify').child('artist').get().val().keys())

	# if artist no longer exists in user database, remove album data from storage
	if artist_list != storage_list:
		outdated_artist = set(storage_list) - set(artist_list)
		db.child('storage').child('spotify').child('artist').child(list(outdated_artist)[0]).remove()


stream_firebase_notification_changes = db.child('notifications').child('spotify').child('artist').stream(stream_handler)
