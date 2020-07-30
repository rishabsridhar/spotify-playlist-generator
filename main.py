from spotify_manager import SpotifyOAuthManager, main_script as spotify_ms
from reddit_bot import main_script as reddit_ms
import sys


def get_all_reddit_songs(spotify_username='', limit=99, clean=True):
    sp = SpotifyOAuthManager(spotify_username)
    reddit_songs = reddit_ms()[:limit]
    track_ids = []
    for track_info in reddit_songs:
        search_query = track_info['song'] + ' ' + track_info['artist']
        track_id = sp.get_track_id(search_query)
        if track_id not in [None, '']:
            if clean and sp.is_explicit(track_id): continue
            track_ids.append(track_id)

    return {
        'track_ids': track_ids,
        'spotify_username': spotify_username
    }

def get_reddit_songs_by_genre(genres, 
                            has_all=False, 
                            spotify_username='', 
                            limit=99, 
                            category='hot',
                            clean=True,
                            playlist_name='Reddit\'s r/listentothis Playlist'):

    sp = SpotifyOAuthManager(spotify_username)
    reddit_songs = reddit_ms(limit, category)
    track_ids = []
    for track_info in reddit_songs:
        search_query = track_info['song'] + ' ' + track_info['artist']
        track_id = sp.get_track_id(search_query)
        if track_id not in [None, '']:
            if clean and sp.is_explicit(track_id): continue
            if has_all:
                has_genres = True
                for g in track_info['genres']:
                    if g not in genres:
                        has_genres = False
                        break
                if has_genres:
                    track_ids.append(track_id)
            else:
                has_genres = False
                for g in track_info['genres']:
                    if g in genres:
                        has_genres = True
                        break
                if has_genres:
                    track_ids.append(track_id)
    return {
        'track_ids': track_ids,
        'spotify_username': spotify_username
    }

def parse_reddit_data(data, playlist_name):
    sp = SpotifyOAuthManager(data['spotify_username'])
    track_ids = []
    for i in data:
        track_ids.append(i['id'])
    return {
        'playlist_id': sp.get_playlist_id(playlist_name),
        'track_ids': track_ids,
        'spotify_username': spotify_username
    }


def add_reddit_songs(data, playlist_name):
    sp = SpotifyOAuthManager(data['spotify_username'])
    sp.add_tracks(sp.get_playlist_id(playlist_name), data['track_ids'], data['spotify_username'])



def get_data_with_ids(list_track_ids, spotify_username=''):
    sp = SpotifyOAuthManager(spotify_username)
    if 50 < len(list_track_ids) < 100:
        l = sp.get_tracks_info(list_track_ids[:50])
        l.extend(sp.get_tracks_info(list_track_ids[50:]))
        return l
    if len(list_track_ids) > 50:
        l = []
        for i in range(len(l)//50):
            l.extend(sp.get_tracks_info(list_track_ids[50*i:50*(i+1)]))
        return l
    return sp.get_tracks_info(list_track_ids)

def add_generated_tracks(parsed_data, generated_tracks):
    username = parsed_data['spotify_username']
    sp = SpotifyOAuthManager(username)
    playlist_id = sp.get_playlist_id(playlist_name=parsed_data['playlist_name'], username=username)
    sp.add_tracks(playlist_id, generated_tracks, username)


def create_playlist():
    spotify_ms()


if __name__=='__main__':
    spotify_username = input('Enter your username: ')
    data = get_reddit_songs_by_genre(genres=['indie', 'pop', 'rock'], 
                                    has_all=False,
                                    limit=99, 
                                    spotify_username=spotify_username, 
                                    category='new')
    add_reddit_songs(data, 'Reddit playlist')
    


