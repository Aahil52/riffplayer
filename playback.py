import os
import logging
from gpiozero import Button, LED, LEDBoard
import spotipy
from spotipy.oauth2 import SpotifyOAuth


logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = 'https://localhost/riffplayer'
SCOPE = 'user-read-playback-state,user-modify-playback-state'
DEFAULT_DEVICE_ID = '0bb4d726656ae60024e260e346f6dedf33f2348d'

toggle_playback_btn = Button(13)
next_btn = Button(6)
previous_btn = Button(19)
shuffle_btn = Button(26)
repeat_btn = Button(5)

shuffle_led = LED(21)
repeat_leds = LEDBoard(20, 16)

def update_indicator_leds(curr_plbk):
    if curr_plbk['shuffle_state']:
        shuffle_led.on()
    else:
        shuffle_led.off()
    if curr_plbk['repeat_state'] == 'context':
        repeat_leds.value = (1, 0)
    elif curr_plbk['repeat_state'] == 'track':
        repeat_leds.value = (1, 1)
    else:
        repeat_leds.off()

def toggle_playback(is_playing, curr_device_id, target_device_id):
    if is_playing and curr_device_id == target_device_id:
        sp.pause_playback()
        logging.info("Playback paused")
    elif curr_device_id == target_device_id:
        sp.start_playback()
        logging.info("Playback started")
    else:
        sp.transfer_playback(target_device_id)
        logging.info("Playback transferred")

def toggle_shuffle(shuffle_state):
    if shuffle_state is None:
        logging.info("Shuffle not set: player inactive")
    else:
        shuffle_led.value = int(not shuffle_state)
        sp.shuffle(not shuffle_state)
        logging.info("Shuffle set to " + str(not shuffle_state))

def cycle_repeat(repeat_state):
    if repeat_state == 'off':
        repeat_leds.value = (1, 0)
        sp.repeat('context')
        logging.info("Repeat set to 'context'")
    elif repeat_state == 'context':
        repeat_leds.value = (1, 1)
        sp.repeat('track')
        logging.info("Repeat set to 'track'")
    elif repeat_state == 'track':
        repeat_leds.value = (0, 0)
        sp.repeat('off')
        logging.info("Repeat set to 'off'")
    elif repeat_state is None:
        logging.info("Repeat not set: player inactive")

def playback_control(curr_plbk, target_device_id=DEFAULT_DEVICE_ID):
    if toggle_playback_btn.is_pressed:
        toggle_playback(curr_plbk['is_playing'], curr_plbk['device']['id'], target_device_id)
    elif next_btn.is_pressed:
        sp.next_track()
        logging.info("Skipped to next track")
    elif previous_btn.is_pressed:
        sp.previous_track()
        logging.info("Back to previous track")
    elif shuffle_btn.is_pressed:
        toggle_shuffle(curr_plbk['shuffle_state'])
    elif repeat_btn.is_pressed:
        cycle_repeat(curr_plbk['repeat_state'])

while True:
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE))

        while True:
            curr_plbk = sp.current_playback(market='US')
            if curr_plbk is None:
                # Assume these values as default
                curr_plbk = {'is_playing': None, 'shuffle_state': None, 'repeat_state': None, 'device': {'id': None}}

            update_indicator_leds(curr_plbk)
            playback_control(curr_plbk)
    except Exception:
        pass