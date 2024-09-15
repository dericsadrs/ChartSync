# Spotify Playlist Maker

## Overview
Spotify Playlist Maker is a Python application that automatically creates a playlist on Spotify using the latest Billboard Top 100 songs. The project interacts with both Spotify's API and Billboard's chart data to gather the latest tracks and add them to a user-defined playlist.

## Features
- Scrapes the latest Billboard Top 100 songs.
- Uses the Spotify API to create a public playlist.
- Searches for Billboard songs on Spotify by artist and title.
- Adds found tracks to the playlist.

## Project Structure

- **app.py**: Entry point for the application. It initializes and runs the Playlist Manager to create a Spotify playlist from Billboard Top 100 songs.
- **config.py**: Handles environment variable configuration for API keys, including Spotify API credentials.
- **billboard_scraper.py**: Contains functionality to scrape the Billboard Top 100 chart for song and artist data.
- **playlist_manager.py**: Manages the process of searching for Billboard songs on Spotify, creating a playlist, and adding songs to it.
- **spotify_playlist_maker.py**: Handles authentication and interaction with the Spotify API to create playlists and add tracks.

## Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.8 or higher
- `pip` for managing Python packages
- A Spotify Developer account to get API keys
- A `.env` file with Spotify credentials and optionally GPT API key

### API Keys
1. **Spotify API**: You need to register your application on [Spotify Developer](https://developer.spotify.com/dashboard/login) to get the following:
   - `SPOTIPY_CLIENT_ID`
   - `SPOTIPY_CLIENT_SECRET`
   - `SPOTIPY_REDIRECT_URI`
   
   These should be stored in a `.env` file:
   ```
   SPOTIPY_CLIENT_ID=<your_spotify_client_id>
   SPOTIPY_CLIENT_SECRET=<your_spotify_client_secret>
   SPOTIPY_REDIRECT_URI=<your_redirect_uri>
   ```

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Spotify-Playlist-Maker
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the Spotify credentials mentioned above.

4. Run the application:
   ```bash
   python app.py
   ```

## Class Breakdown

### `Config` (config.py)
Handles loading and managing environment variables:
- `__init__`: Initializes the class, loads the `.env` file.
- `_load_env_variables`: Loads variables from the `.env` file.
- `_log_variables`: Logs whether the environment variables were successfully loaded.

### `BillboardScraper` (billboard_scraper.py)
Scrapes the Billboard website for the latest Top 100 songs.
- `get_top_100`: Returns a list of songs and artists from the Billboard chart.

### `SpotifyPlaylistMaker` (spotify_playlist_maker.py)
Handles Spotify API interactions including authentication, playlist creation, and track addition.
- `authenticate`: Authenticates with Spotify using OAuth 2.0.
- `create_playlist`: Creates a public Spotify playlist for the user.
- `add_tracks_to_playlist`: Adds tracks to the playlist using Spotify URIs.
- `search_song`: Searches for a song on Spotify using artist and track name.

### `PlaylistManager` (playlist_manager.py)
Coordinates between BillboardScraper and SpotifyPlaylistMaker.
- `create_billboard_playlist`: Scrapes Billboard Top 100 songs, searches for them on Spotify, and creates a playlist with those tracks.

## Example Playlist

Here is an example playlist created using the Spotify Playlist Maker, which automatically gathers songs from Billboard's Top 100:
![Screenshot 2024-09-15 at 11 09 53 AM](https://github.com/user-attachments/assets/c5bce71d-07e3-41a9-bf79-c56671493086)

This playlist contains 85 songs, totaling approximately 4 hours and 27 minutes of music, and was generated entirely by scraping Billboard's latest Top 100 songs.

## How to Use

1. Run the application with:
   ```bash
   python app.py
   ```

2. The application will:
   - Scrape the Billboard Top 100 songs.
   - Search for the songs on Spotify.
   - Create a new playlist and add the songs to the playlist.

## Notes
- Ensure your Spotify Developer app is set up correctly for authentication.
- The app will prompt you to authenticate via the browser on the first run.

## License
MIT License

---
