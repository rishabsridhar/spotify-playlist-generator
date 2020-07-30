import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from urllib.parse import urlencode
import sys
from random import shuffle

try:
    with open('client_credentials.txt', 'r') as my_file:
        s = ''
        for line in my_file:
            s += line.rstrip() + ' '
        creds = tuple(s.split())
        SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET = creds
except FileNotFoundError:
    print('client_credentials.txt is not in the current directory.')
    sys.exit()
    

class SpotifyOAuthManager:
    """Spotify API Manager with OAuth Flow. Requires user authentication for the given scopes."""

    scopes = [
        'user-modify-playback-state', 
        'user-read-playback-state', 
        'playlist-read-private', 
        'playlist-modify-private', 
        'playlist-modify-public', 
        'user-top-read'
        ]

    def __init__(self, username, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri='http://localhost:8888/callback'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        scope = ' '.join(self.scopes)
        token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, redirect_uri)
        self.sp = spotipy.Spotify(auth=token)

    def get_artist(self, search_query):
        data = self.sp.search(search_query, type='artist')
        return {} if len(data['artists']['items'][0]) == 0 else data['artists']['items'][0]

    def get_artists(self, search_query):
        data = self.sp.search(search_query, type='artist')
        return {} if len(data['artists']['items']) == 0 else data['artists']['items']

    def get_artist_id(self, search_query):
        data = self.sp.search(search_query, type='artist')
        try:
            return '' if len(data['artists']['items'][0]) == 0 else data['artists']['items'][0]['id']
        except IndexError:
            return None

    
    def get_track(self, search_query):
        data = self.sp.search(search_query, type='track')
        return {} if len(data['tracks']['items'][0]) == 0 else data['tracks']['items'][0]

    def get_tracks(self, search_query):
        data = self.sp.search(search_query, type='track')
        return {} if len(data['tracks']['items']) == 0 else data['tracks']['items']

    def get_track_id(self, search_query):
        data = self.sp.search(search_query, type='track')
        try:
            return '' if len(data['tracks']['items'][0]) == 0 else data['tracks']['items'][0]['id']
        except IndexError:
            return None

    def get_tracks_info(self, list_track_ids):
        return self.sp.tracks(list_track_ids)['tracks']
        

    def is_explicit(self, track_id):
        track_info = self.sp.track(track_id)
        return track_info['explicit']


    def get_top_tracks(self, artist):
        if isinstance(artist, dict):
            top = self.sp.artist_top_tracks(artist['uri'])
            return [t for t in top['tracks']]
        elif isinstance(artist, str):
            top = self.sp.artist_top_tracks(artist)
            return [t for t in top['tracks']]


    def get_devices(self):
        devices = self.sp.devices()
        return devices['devices']

    def start(self, device_id):
        self.sp.start_playback(device_id)

    def pause(self, device_id):
        self.sp.pause_playback(device_id)


    def create_playlist(self, playlist_name, public='false', username=''):
        public = str(public).lower() if isinstance(public, bool) else public
        username = self.username if username=='' else username
        self.sp.user_playlist_create(username, playlist_name)
        return self.get_playlist_id(playlist_name, username)

    def get_playlist_id(self, playlist_name, username=''):
        username = self.username if username=='' else username
        playlists = self.sp.user_playlists(username)

        for p in playlists['items']:
            if p['name'] == playlist_name:
                return p['id']
        return self.create_playlist(playlist_name, username)


    def add_tracks(self, playlist_id, list_track_ids, username=''):
        username = self.username if username=='' else username
        self.sp.user_playlist_add_tracks(username, playlist_id, list_track_ids[:99])


    def recommendations(self, seed_tracks=None, seed_artists=None, seed_genres=None, limit=20):
        return self.sp.recommendations(seed_tracks=seed_tracks, seed_artists=seed_artists, seed_genres=seed_genres, limit=limit)

    def recommendation_ids(self, recommendations={'tracks':[]}, explicit=False):
        list_track_ids = []
        for track in recommendations['tracks']:
            if not explicit and track['explicit']:
                continue   
            list_track_ids.append(track['id'])
        return list_track_ids

    def recommendation_genre_seeds(self):
        return self.sp.recommendation_genre_seeds()['genres']


    def create_randomized_playlist(self, playlist_id):
        playlists = self.sp.user_playlists(self.username)
        playlist = None
        for p in playlists['items']:
            if p['id'] == playlist_id:
                playlist = p
        print(playlist)



def generate_playlist(data, explicit, limit=50):
    username = data['spotify_username']
    playlist_name = data['playlist_name']
    artists = data['artists']
    tracks = data['tracks']
    genres = data['genres']

    main_tracks = []
    artist_ids = []
    track_ids = []
    sp = SpotifyOAuthManager(username)
    if artists != ['']:
        print('artist', artist_ids)
        artist_ids = [sp.get_artist_id(i) for i in artists if sp.get_artist_id(i) != None]
    if tracks != ['']:
        track_ids = [sp.get_track_id(i) for i in tracks if sp.get_track_id(i) != None]
    seed_genres = [i for i in genres if i in sp.recommendation_genre_seeds()]
    
    #playlist_id = sp.get_playlist_id(playlist_name)

    top_track_ids = []
    lim = 5
    for a in artist_ids:
        for n,i in enumerate(sp.get_top_tracks(a)):
            if n > lim:
                break
            top_track_ids.append(i['id'])
    
    if len(artist_ids) != 0:
        main_tracks.extend(top_track_ids)

    if len(track_ids) != 0:
        main_tracks.extend(track_ids)

    artist_ids = None if artist_ids==[] else artist_ids
    seed_genres = None if seed_genres==[] else seed_genres
    track_ids = None if track_ids==[] else track_ids

    recs = sp.recommendations(seed_artists=artist_ids, seed_genres=seed_genres, seed_tracks=track_ids, limit=limit)

    list_track_ids = sp.recommendation_ids(recs, explicit)
    if len(list_track_ids) != 0:
        main_tracks.extend(list_track_ids)

    shuffle(main_tracks)

    return main_tracks


def main_script():
    username = input('Enter your username: ')
    sp = SpotifyOAuthManager(username)
    artist_ids = [] 
    while True:
        name = input('Enter an artist name (\' \' to exit): ')
        if name=='': break
        artist_ids.append(sp.get_artist_id(name))

    seed_genres = []
    while True:
        name = input('Enter an genre (\' \' to exit): ')
        if name=='': break
        if name in sp.recommendation_genre_seeds():
            seed_genres.append(name)
        else:
            print('Not a valid genre.')

    track_ids = []
    while True:
        name = input('Enter an track name (\' \' to exit): ')
        if name=='': break
        track_ids.append(sp.get_track_id(name))
    
    playlist_name = input('Enter the playlist name: ')
    playlist_name = 'SPOTIPY_TEST' if playlist_name=='' else playlist_name
    playlist_id = sp.get_playlist_id(playlist_name)

    list_track_ids = []
    lim = 5
    for a in artist_ids:
        for n,i in enumerate(sp.get_top_tracks(a)):
            if n > lim:
                break
            list_track_ids.append(i['id'])
    
    if len(artist_ids) != 0:
        sp.add_tracks(playlist_id, list_track_ids)

    if len(track_ids) != 0:
        sp.add_tracks(playlist_id, track_ids)

    artist_ids = None if artist_ids==[] else artist_ids
    seed_genres = None if seed_genres==[] else seed_genres
    track_ids = None if track_ids==[] else track_ids

    recs = sp.recommendations(seed_artists=artist_ids, seed_genres=seed_genres, seed_tracks=track_ids, limit=50)

    explicit = input('Are you ok with explicit music? (Y/N): ').lower()
    explicit = True if explicit[0]=='y' else False
    list_track_ids = sp.recommendation_ids(recs, explicit=explicit)
    playlist_id = sp.get_playlist_id(playlist_name)
    sp.add_tracks(playlist_id, list_track_ids)



if __name__=='__main__':
    main_script()

