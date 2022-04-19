import os
import logging
from time import sleep
import nfc
import spotipy
from spotipy.oauth2 import SpotifyOAuth


logging.basicConfig(filename="riffplayer.log", format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

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
            sp.add_to_queue(record.uri)
            logging.info("Track added to the queue")
        except Exception:
            pass
    elif record.uri.startswith("spotify:album:") or record.uri.startswith("spotify:playlist:") or record.uri.startswith("spotify:artist:"):
        try:
            sp.start_playback(context_uri=record.uri)
            logging.info("Collection playback started")
        except Exception:
            pass
    else:
        logging.warning("NDEF record 0 is not a valid/supported Spotify URI")
    # Returning True prevents the device from repeatedly reading the same tag
    return True

# For Elechouse PN532v1.6 at /dev/ttyS0 over UART
clf = nfc.ContactlessFrontend('tty:S0')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'), client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'), redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'), scope='user-read-playback-state,user-modify-playback-state'))

while True:
    return_value = clf.connect(rdwr={'on-connect': tapped, 'beep-on-connect': False})
    # clf.connect returns False on keyboard interrupt instead of exiting script
    if return_value is False:
        print("")
        break
    sleep(0.1)

clf.close()