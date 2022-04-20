import os
import logging
import toml
from time import sleep
import nfc
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_target_device_id():
    with open('config.toml') as f:
            return toml.load(f)['device']['target_device_id']

def tapped(tag):
    if tag.ndef is None:
        logging.warning("Tag has no NDEF records")
        return
    record = tag.ndef.records[0]
    if record.type != 'urn:nfc:wkt:U':
        logging.warning("NDEF record 0 is not a URI")
        return
    if record.uri.startswith("spotify:track:"):
        try:
            sp.start_playback(device_id=get_target_device_id(), uris=[record.uri])
            logging.info("Track playback started")
        except Exception:
            pass
    elif record.uri.startswith("spotify:album:") or record.uri.startswith("spotify:playlist:") or record.uri.startswith("spotify:artist:"):
        try:
            sp.start_playback(device_id=get_target_device_id(), context_uri=record.uri)
            logging.info("Collection playback started")
        except Exception:
            pass
    else:
        logging.warning("NDEF record 0 is not a valid/supported Spotify URI")
    # Returning True prevents the device from repeatedly reading the same tag
    return True

with open('config.toml') as f:
    config = toml.load(f)

logging.basicConfig(filename="riffplayer.log", format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config['spotipy']['client_id'], client_secret=config['spotipy']['client_secret'], redirect_uri=config['spotipy']['redirect_uri'], scope='user-read-playback-state,user-modify-playback-state'))

# For Elechouse PN532v1.6 at /dev/ttyS0 over UART
with nfc.ContactlessFrontend('tty:S0') as clf:
    while True:
        return_value = clf.connect(rdwr={'on-connect': tapped, 'beep-on-connect': False})
        # clf.connect returns False on keyboard interrupt instead of exiting script
        if return_value is False:
            print("")
            break
        sleep(0.1)