import time

import spotipy
from flask import Flask, redirect, request, session, url_for
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'qdjqbd@348480#5$knfri'

TOKEN_INFO = 'token_info'

@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('save_discover_weekly', _external=True))

@app.route('/saveDiscoverWeekly')
def save_discover_weekly():
    try:
        token_info = get_token()
    except Exception as e:
        print("User not logged in:", e)
        return redirect('/')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_id = sp.current_user()['id']
    
    discover_weekly_playlist_id = None
    saved_weekly_playlist_id = None
    current_playlists = sp.current_user_playlists()['items']
    
    for playlist in current_playlists:
        if playlist['name'] == "Discover Weekly":
            discover_weekly_playlist_id = playlist['id']
        if playlist['name'] == "Saved Weekly":
            saved_weekly_playlist_id = playlist['id']
            
    if not discover_weekly_playlist_id:
        return "Discover Weekly not found"
    
    if not saved_weekly_playlist_id:
        new_playlist = sp.user_playlist_create(user_id, 'Saved Weekly', public=True)
        saved_weekly_playlist_id = new_playlist['id']
        
    discover_weekly_playlist = sp.playlist_items(discover_weekly_playlist_id)
    song_uris = [song['track']['uri'] for song in discover_weekly_playlist['items']]
    
    sp.user_playlist_add_tracks(user_id, saved_weekly_playlist_id, song_uris)
    
    return "SUCCESS!!!"

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        return redirect(url_for('login'))
        
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
        session[TOKEN_INFO] = token_info
        
    return token_info

def create_spotify_oauth():    
    return SpotifyOAuth(
        client_id="159008d3edf04624b2d4890c6673d1ae",
        client_secret="7bc5bc7bee4349e0beb87f29184febfe",
        redirect_uri=url_for('redirect_page', _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )

if __name__ == '__main__':
    app.run(debug=True)
