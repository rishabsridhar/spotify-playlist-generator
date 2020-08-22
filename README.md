# spotify-playlist-generator
A Web App that can create Spotify Playlists by either scraping songs from Reddit or by generating a playlist based on user-inputted data (artists, tracks, genres).

Currently the web app is functional and can successfully generate playlists based on the subreddit r/listentothis or on user-inputted data. You should enter your Spotify Username/User ID as it may not be the same as your display name. Requires Spotify Premium.

# setup
1. Create a text file called client_credentials.txt and have line 1 be your client_id and line 2 be your client_secret.
2. If you want Reddit songs, fill in config.py with your reddit bot credentials as stated.
3. Run app.py and the website will be hosted on http://localhost:5000
4. To use OAuth, Spotify will redirect you to login and give this application access to your library in order to create/add to existing playlists.

# How it Works

## app.py
Creates the Web App using Flask and handles requests made from the frontend. It processes requests using main.py and spotify_manager.py. Takes JSON data and parses it to be used in other backend modules or sent to the frontend. Stores usernames and playlist names in global variables as they are used in separate requests. Uses render_template to create webpages for the user.

## config.py
Stores the user Reddit credentials and information about the reddit bot.

## main.py
Creates playlists based on information scraped by reddit_bot.py and through user-inputted information. Uses spotify_manager.py to actually generate the playlist and sends the information to app.py as a dictionary.

## reddit_bot.py
Scrapes data from the subreddit r/listentothis by parsing the titles of posts, which is sorted by 'hot' by default. It uses the Reddit API Wrapper (PRAW) to get the information.

## spotify_manager.py
Uses the Spotify Web API and Spotipy to create playlists for the user. It uses OAuth Authorization Protocol to access the API. This module has more uses than what this project utilizes, as it can change user playback and get devices. For the purposes of this project, it gets tracks/artists ids and song recommendations. It can generate playlists and create/add to current playlists based on certain tracks/artists/genres using mutual recursion.

## static
Stores all of the Javascript and CSS for the webpages. The files pg_script.js and reddit_script.js use AJAX to send JSON files to app.py for processing and receives JSONs to use accordingly (e.g. display playlist songs on screen before adding them).

## templates
Stores the HTML5 for the homepage, the Reddit generator, and the Standard playlist generator. The latter two use Jinja2 syntax to display a list of songs before adding them to a playlist.
