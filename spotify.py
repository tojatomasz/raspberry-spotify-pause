import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = ''
scope = 'user-modify-playback-state user-read-playback-state'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope,
                                               open_browser=False))

def current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def is_music_playing(retry=3, delay=1):
    while retry > 0:
        try:
            playback_state = sp.current_playback()
            return playback_state is not None and playback_state['is_playing']
        except (spotipy.exceptions.SpotifyException) as e:
            print(f"{current_time()} - Blad podczas sprawdzania stanu odtwarzania: {e}")
            time.sleep(delay)
            retry -= 1
    return False

def pause_spotify():
    if is_music_playing():
        try:
            sp.pause_playback()
            print(f"{current_time()} - Muzyka została zapauzowana.")
        except Exception as e:
            print(f"{current_time()} - Blad podczas pauzowania Spotify:", e)

def resume_spotify():
    if not is_music_playing():
        try:
            sp.start_playback()
            print(f"{current_time()} - Muzyka zostala wznowiona.")
        except Exception as e:
            print(f"{current_time()} - Blad podczas wznawiania Spotify:", e)

door_state = None

try:
    while True:
        current_state = GPIO.input(17)
        if current_state != door_state:
            if current_state == True:
                print(f"{current_time()} - Drzwi zostaly otwarte.")
                pause_spotify()
            else:
                print(f"{current_time()} - Drzwi zostaly zamkniete.")
                resume_spotify()
            door_state = current_state
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
