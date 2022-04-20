import toml
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth

with open('/home/riff/riffplayer/config.toml') as f:
    config = toml.load(f)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config['spotipy']['client_id'], client_secret=config['spotipy']['client_secret'], redirect_uri=config['spotipy']['redirect_uri'], scope='user-read-playback-state,user-modify-playback-state'))

res = sp.current_playback(market='US')
pprint(res)
