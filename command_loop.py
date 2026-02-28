# import modules
import os, subprocess



os.system('python3 google-drive/work/AnyAlert/spotify_loop.py')
os.system('python3 google-drive/work/AnyAlert/firebase_cleaner.py')
os.system('python3 google-drive/work/AnyAlert/notification_handler.py')


process_list = subprocess.check_output(['pgrep -af python'])

# python "google drive"//work//anyalert//spotify_loop.py # windows