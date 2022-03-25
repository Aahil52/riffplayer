import os
from gpiozero import Button
from gpiozero import LED
from gpiozero import LEDBoard
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def toggle_playback(is_playing):
    if is_playing == False:
        sp.start_playback(device_id=DEVICE_ID)
        print("Playback started")
    else:
        sp.pause_playback(device_id=DEVICE_ID)
        print("Playback paused")

def cycle_repeat(repeat_state):
    if repeat_state == 'off':
        sp.repeat('context', device_id=DEVICE_ID)
        print("Repeat set to 'context'")
    elif repeat_state == 'context':
        sp.repeat('track', device_id=DEVICE_ID)
        print("Repeat set to 'track'")
    elif repeat_state == 'track':
        sp.repeat('off', device_id=DEVICE_ID)
        print("Repeat set to 'off'")

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = 'https://localhost/player'
SCOPE = 'user-read-playback-state,user-modify-playback-state'
DEVICE_ID = '0bb4d726656ae60024e260e346f6dedf33f2348d'

toggle_playback_btn = Button(13)
next_btn = Button(6)
previous_btn = Button(19)
shuffle_btn = Button(26)
repeat_btn = Button(5)

while True:
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE))

        while True:
            curr_plbk = sp.current_playback(market='US')
            if curr_plbk == None:
                # Assume these values
                curr_plbk = {'is_playing': False, 'repeat_state': 'off', 'shuffle_state': False}

            if toggle_playback_btn.is_pressed:
                toggle_playback(curr_plbk['is_playing'])
            elif next_btn.is_pressed:
                sp.next_track(device_id=DEVICE_ID)
                print("Skipped to next track")
            elif previous_btn.is_pressed:
                sp.previous_track(device_id=DEVICE_ID)
                print("Back to previous track")
            elif shuffle_btn.is_pressed:
                sp.shuffle(not curr_plbk['shuffle_state'], device_id=DEVICE_ID)
                print("Shuffle set to " + str(not curr_plbk['shuffle_state']))
            elif repeat_btn.is_pressed:
                cycle_repeat(curr_plbk['repeat_state'])
    except Exception as e:
        print(e)
        pass