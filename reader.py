import os
import sys
import logging
import toml
from time import sleep
import nfc
import spotipy
from spotipy.oauth2 import SpotifyOAuth


with open('config.toml') as f:
    config = toml.load(f)

logging.basicConfig(filename="riffplayer.log", format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config['spotipy']['client_id'], client_secret=config['spotipy']['client_secret'], redirect_uri=config['spotipy']['redirect_uri'], scope='user-read-playback-state,user-modify-playback-state'))

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

def main():
    # Path determined by config
    with nfc.ContactlessFrontend(config['reader']['path']) as clf:
        while True:
            rdwr_options = {
                'on-connect': tapped,
                'interval': 0.5,
                'beep-on-connect': False
            }
            return_value = clf.connect(rdwr=rdwr_options)
            # clf.connect returns False on keyboard interrupt instead of exiting script
            # ** Beware, may return False on other errors **
            if  return_value is False and os.getpgrp() == os.tcgetpgrp(sys.stdout.fileno()):
                print("")
                break
            sleep(0.1)

if __name__ == '__main__':
    main()
