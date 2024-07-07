# Music Vault
This Flask web application allows users to automatically save tracks from their Spotify Discover Weekly playlist to a new playlist named "Saved Weekly". Utilizing the Spotipy library, the application interacts with the Spotify Web API to authenticate users and manage their playlists.

# Features
- User Authentication: OAuth 2.0 authentication with Spotify to securely access user data.
- Discover Weekly Tracking: Automatically detects the user's Discover Weekly playlist.
- Playlist Creation: Creates a new playlist named "Saved Weekly" if it doesn't already exist.
- Song Transfer: Transfers songs from Discover Weekly to Saved Weekly with a single click

# Usage
- Open your web browser and navigate to http://localhost:5000.
- Log in to Spotify and grant the necessary permissions.
- The application will automatically detect your Discover Weekly playlist and save its tracks to a new or existing "Saved Weekly" playlist.
