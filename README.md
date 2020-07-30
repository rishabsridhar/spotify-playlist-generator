# spotify-playlist-generator
A Web App that can create Spotify Playlists by scraping songs from Reddit and by user-inputted data (artists, tracks, genres).

# setup
1. Create a text file called client_credentials.txt and have line 1 be your client_id and line 2 be your client_secret.
2. Fill in config.py with your reddit bot credentials as stated if you want reddit_bot functionality.
3. Run app.py and the website will be hosted on http://localhost:5000


Currently the web app is not pretty, but it is functional and can successfully generate playlists based on the subreddit r/listentothis or on user-inputted data. You should enter your Spotify Username/User ID as it may not be the same as your display name. Requires Spotify Premium.
