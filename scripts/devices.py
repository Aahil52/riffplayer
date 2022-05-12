import toml
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth

with open('/home/riff/riffplayer/config.toml') as f:
    config = toml.load(f)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config['spotipy']['client_id'], client_secret=config['spotipy']['client_secret'], redirect_uri=config['spotipy']['redirect_uri'], scope='user-read-playback-state,user-modify-playback-state'))

devices = sp.devices()['devices']

for i, device in enumerate(devices):
    print(f"{i}: {device['name']}")

while True:
    try:
        sel = int(input("Select Device: "))

        keys = ['id', 'name', 'type']
        for key in keys:
            print(f"{key}: {devices[sel][key]}")
    except Exception as e:
        print(e)
        continue
    break