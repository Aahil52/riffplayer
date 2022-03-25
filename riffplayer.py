import os
from gpiozero import Button
from gpiozero import LED
from gpiozero import LEDBoard
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def update_indicator_leds(curr_plbk):
    if curr_plbk['shuffle_state'] == False:
        shuffle_led.off()
    elif curr_plbk['shuffle_state'] == True:
        shuffle_led.on()
    if curr_plbk['repeat_state'] == 'off':
        repeat_leds.value = (0, 0)
    elif curr_plbk['repeat_state'] == 'context':
        repeat_leds.value = (1, 0)
    elif curr_plbk['repeat_state'] == 'track':
        repeat_leds.value = (1, 1)

def toggle_playback(is_playing):
    if is_playing == False:
        sp.start_playback(device_id=DEVICE_ID)
        print("Playback started")
    else:
        sp.pause_playback(device_id=DEVICE_ID)
        print("Playback paused")

def toggle_shuffle(shuffle_state):
    if shuffle_state == None:
        print("Shuffle not set: player idle")
    else:
        shuffle_led.value = int(not shuffle_state)
        sp.shuffle(not shuffle_state, device_id=DEVICE_ID)
        print("Shuffle set to " + str(not shuffle_state))

def cycle_repeat(repeat_state):
    if repeat_state == 'off':
        repeat_leds.value = (1, 0)
        sp.repeat('context', device_id=DEVICE_ID)
        print("Repeat set to 'context'")
    elif repeat_state == 'context':
        repeat_leds.value = (1, 1)
        sp.repeat('track', device_id=DEVICE_ID)
        print("Repeat set to 'track'")
    elif repeat_state == 'track':
        repeat_leds.value = (0, 0)
        sp.repeat('off', device_id=DEVICE_ID)
        print("Repeat set to 'off'")
    elif repeat_state == None:
        print("Repeat not set: player idle")

def playback_control(curr_plbk):
    if toggle_playback_btn.is_pressed:
        toggle_playback(curr_plbk['is_playing'])
    elif next_btn.is_pressed:
        sp.next_track(device_id=DEVICE_ID)
        print("Skipped to next track")
    elif previous_btn.is_pressed:
        sp.previous_track(device_id=DEVICE_ID)
        print("Back to previous track")
    elif shuffle_btn.is_pressed:
        toggle_shuffle(curr_plbk['shuffle_state'])
    elif repeat_btn.is_pressed:
        cycle_repeat(curr_plbk['repeat_state'])

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

shuffle_led = LED(21)
repeat_leds = LEDBoard(20, 16)

while True:
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE))

        while True:
            curr_plbk = sp.current_playback(market='US')
            if curr_plbk == None:
                # Assume these values
                curr_plbk = {'is_playing': False, 'shuffle_state': None, 'repeat_state': None}

            update_indicator_leds(curr_plbk)
            playback_control(curr_plbk)
    except Exception as e:
        print(e)
        pass