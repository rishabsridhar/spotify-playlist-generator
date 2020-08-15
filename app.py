from flask import Flask, render_template, request, jsonify
from main import get_all_reddit_songs, add_reddit_songs, get_data_with_ids, parse_reddit_data, add_generated_tracks
from spotify_manager import generate_playlist
import json
import sys
import time
import webbrowser

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/reddit')
def reddit():
    return render_template('reddit.html', data=None)

@app.route('/playlist_generator')
def playlist_generator():
    return render_template('playlist_generator.html', data=None)



def parse_input_data(data):
    raw_artists = data['raw_artists']
    raw_tracks = data['raw_tracks']
    raw_genres = data['raw_genres']
    if raw_artists == '' and raw_tracks == '' and raw_genres == '':
        return {}
    artists = [i.lstrip().rstrip() for i in raw_artists.split(',')]
    tracks = [i.lstrip().rstrip() for i in raw_tracks.split(',')]
    genres = [i.lstrip().rstrip().lower() for i in raw_genres.split(',')]
    return {
        'spotify_username': data['spotify_username'],
        'playlist_name': data['playlist_name'],
        'artists': artists,
        'tracks': tracks,
        'genres': genres
    }


# Global variables so that the user does not need to enter information twice
global parsed_data
global generated_tracks
@app.route('/_get_playlist', methods=['GET', 'POST'])
def _get_playlist():
    global parsed_data
    parsed_data = parse_input_data(json.loads(request.get_data()))
    if parsed_data == {}:
        return render_template('playlist_generator.html', data=None)
    list_track_ids = generate_playlist(parsed_data, explicit=False)
    print('LENGTH: ',len(list_track_ids))
    data = get_data_with_ids(list_track_ids)
    global generated_tracks
    generated_tracks = list_track_ids
    return render_template('playlist_generator.html', data=data)

@app.route('/_add_songs', methods=['GET', 'POST'])
def _add_songs():
    global parsed_data
    global generated_tracks
    add_generated_tracks(parsed_data, generated_tracks)
    time.sleep(3)
    return jsonify({})

    

# Global variables so that the user does not need to enter information twice
global reddit_songs_data
global reddit_playlist_name
@app.route('/_get_reddit_songs', methods=['GET', 'POST'])
def _get_reddit_songs():
    user_data = json.loads(request.get_data())
    global reddit_playlist_name
    reddit_playlist_name = user_data['playlist_name']
    username = user_data['spotify_username']
    global reddit_songs_data
    reddit_songs_data = get_all_reddit_songs(username)
    track_ids = reddit_songs_data['track_ids']
    data = get_data_with_ids(track_ids, username)
    return render_template('reddit.html', data=data)

@app.route('/_add_reddit_songs', methods=['GET', 'POST'])
def _add_reddit_songs():
    user_data = json.loads(request.get_data())
    global reddit_playlist_name
    playlist_name = user_data['playlist_name'] if reddit_playlist_name=='' else reddit_playlist_name
    global reddit_songs_data
    add_reddit_songs(reddit_songs_data, playlist_name)
    time.sleep(3)
    return jsonify({})


if __name__ == '__main__':
    #webbrowser.open_new_tab('http://localhost:5000')
    app.run(port=5000)
    