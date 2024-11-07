# Music Chart Playlist Creator

This project is a Python application that scrapes music charts and creates Spotify playlists based on the scraped data.

## Classes and Functions Description

### `Config` (config.py)
- Manages environment variables and configuration settings.
- Methods:
  - `get_client_id()`: Returns the Spotify Client ID.
  - `get_client_secret()`: Returns the Spotify Client Secret.
  - `get_redirect_uri()`: Returns the Spotify Redirect URI.
  - `get_gpt_key()`: Returns the GPT API key.

### `Scraper` (scraper.py)
- Scrapes music charts using Playwright.
- Methods:
  - `get_latest_chart()`: Fetches the latest chart data.
  - `display_songs()`: Displays scraped songs in a human-readable format.

### `SpotifyPlaylistMaker` (spotify_playlist_maker.py)
- Handles Spotify authentication and playlist operations.
- Methods:
  - `authenticate()`: Authenticates with Spotify API.
  - `create_playlist()`: Creates a new Spotify playlist.
  - `add_tracks_to_playlist()`: Adds tracks to a Spotify playlist.
  - `search_song()`: Searches for a song on Spotify.

### `PlaylistManager` (playlist_manager.py)
- Manages the process of creating playlists from scraped chart data.
- Methods:
  - `create_playlist()`: Creates a Spotify playlist based on the specified chart type.

### `GPTOperations` (gpt_operations.py)
- Handles operations related to GPT API.
- Methods:
  - `fetch_songs()`: Fetches songs based on user prompt.
  - `generate_response()`: Generates a response using GPT.

## API Keys and Environment Variables

The following environment variables need to be set in a `.env` file in the `src` directory:

```
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=your_spotify_redirect_uri
GPT_KEY=your_gpt_api_key
```

## How to Run (Prerequisites and Endpoints)

### Prerequisites
1. Python 3.7+
2. Install required packages:
   ```
   pip install spotipy python-dotenv playwright openai
   ```
3. Install Playwright browsers:
   ```
   playwright install
   ```
4. Set up a Spotify Developer account and create an app to get the required API credentials.
5. Set up an OpenAI account to get the GPT API key.

### Running the Application

1. Clone the repository and navigate to the project directory.
2. Create a `.env` file in the `src` directory with the required environment variables.
3. Run the main script:
   ```
   python src/app.py
   ```

### Endpoints

The application doesn't have explicit endpoints as it's not set up as a web service. However, the main functionality can be accessed through the `PlaylistManager` class:

```python
playlist_manager = PlaylistManager()
result = playlist_manager.create_playlist(chart_type="billboard_hot_100")
print(result)
```

## Sample Run

[Leave blank for now]# Music Chart Playlist Creator

This project is a Python application that scrapes music charts and creates Spotify playlists based on the scraped data.

## Classes and Functions Description

### `Config` (config.py)
- Manages environment variables and configuration settings.
- Methods:
  - `get_client_id()`: Returns the Spotify Client ID.
  - `get_client_secret()`: Returns the Spotify Client Secret.
  - `get_redirect_uri()`: Returns the Spotify Redirect URI.
  - `get_gpt_key()`: Returns the GPT API key.

### `Scraper` (scraper.py)
- Scrapes music charts using Playwright.
- Methods:
  - `get_latest_chart()`: Fetches the latest chart data.
  - `display_songs()`: Displays scraped songs in a human-readable format.

### `SpotifyPlaylistMaker` (spotify_playlist_maker.py)
- Handles Spotify authentication and playlist operations.
- Methods:
  - `authenticate()`: Authenticates with Spotify API.
  - `create_playlist()`: Creates a new Spotify playlist.
  - `add_tracks_to_playlist()`: Adds tracks to a Spotify playlist.
  - `search_song()`: Searches for a song on Spotify.

### `PlaylistManager` (playlist_manager.py)
- Manages the process of creating playlists from scraped chart data.
- Methods:
  - `create_playlist()`: Creates a Spotify playlist based on the specified chart type.

### `GPTOperations` (gpt_operations.py)
- Handles operations related to GPT API.
- Methods:
  - `fetch_songs()`: Fetches songs based on user prompt.
  - `generate_response()`: Generates a response using GPT.

## API Keys and Environment Variables

The following environment variables need to be set in a `.env` file in the `src` directory:

```
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=your_spotify_redirect_uri
GPT_KEY=your_gpt_api_key
```

## How to Run (Prerequisites and Endpoints)

### Prerequisites
1. Python 3.7+
2. Install required packages:
   ```
   pip install spotipy python-dotenv playwright openai
   ```
3. Install Playwright browsers:
   ```
   playwright install
   ```
4. Set up a Spotify Developer account and create an app to get the required API credentials.
5. Set up an OpenAI account to get the GPT API key.

### Running the Application

1. Clone the repository and navigate to the project directory.
2. Create a `.env` file in the `src` directory with the required environment variables.
3. Run the main script:
   ```
   python src/app.py
   ```

### Endpoints

The application doesn't have explicit endpoints as it's not set up as a web service. However, the main functionality can be accessed through the `PlaylistManager` class:

```python
playlist_manager = PlaylistManager()
result = playlist_manager.create_playlist(chart_type="billboard_hot_100")
print(result)
```

## Sample Run
![Screenshot 2024-11-06 at 11 08 18 PM](https://github.com/user-attachments/assets/5173a5c8-b602-4654-b1c6-37c90b797aa6)

