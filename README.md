# Music Chart Playlist Creator

This project is a Python application that scrapes music charts and creates Spotify playlists based on the scraped data.

## Features
- Web scraping of music charts (Billboard Hot 100, TikTok Top 50, etc.)
- Automatic Spotify playlist creation
- GPT-powered music recommendations
- Cross-platform support (Windows/Unix)
- Comprehensive test coverage
- RESTful API endpoints

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

## Environment Setup

### Prerequisites
1. Python 3.7+
2. Spotify Developer Account
3. OpenAI API Account
4. Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Music-Chart-Playlist-Creator.git
cd Music-Chart-Playlist-Creator
```

2. Create and set up virtual environment using Make:
```bash
make setup
```

3. Set up environment variables in `.env`:
```plaintext
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=your_spotify_redirect_uri
GPT_KEY=your_gpt_api_key
```

## Running the Application

### Using Make Commands

Start the application:
```bash
make run
```

### Available Make Commands

#### Application Commands
- `make setup`: Set up virtual environment and install dependencies
- `make run`: Start the Flask application
- `make clean`: Clean up virtual environment and generated files
- `make update-deps`: Update dependencies

#### Testing Commands
- `make test-all`: Run all tests
- `make test-models`: Run model tests only
- `make test-services`: Run service tests only
- `make test-coverage`: Run tests with coverage information
- `make test-report`: Generate HTML coverage report
- `make lint`: Run code linting

## API Endpoints

### Billboard Chart Playlists
- `POST /create/playlist/billboard_hot_100`
  - Creates a playlist from Billboard Hot 100
  - Response: 
    ```json
    {
        "message": "Billboard Hot 100 playlist created successfully",
        "status": 201
    }
    ```

- `POST /create/playlist/billboard_tiktok_top_50`
  - Creates a playlist from Billboard TikTok Top 50
  - Response:
    ```json
    {
        "message": "Billboard TikTok Top 50 playlist created successfully",
        "status": 201
    }
    ```

- `POST /create/playlist/billboard_decade_end_hot_100`
  - Creates a playlist from Billboard Decade-End Hot 100
  - Response:
    ```json
    {
        "message": "Billboard Decade End Hot 100 playlist created successfully",
        "status": 201
    }
    ```

### GPT Operations
- `POST /gpt/recommendations`
  - Get song recommendations based on user prompt
  - Request Body:
    ```json
    {
        "prompt": "happy upbeat songs for workout"
    }
    ```
  - Response:
    ```json
    {
        "status": "success",
        "data": [
            {
                "title": "Can't Hold Us",
                "artist": "Macklemore & Ryan Lewis"
            },
            {
                "title": "Uptown Funk",
                "artist": "Mark Ronson ft. Bruno Mars"
            }
            // ... more songs
        ]
    }
    ```

- `POST /gpt/create_playlist`
  - Create a playlist based on GPT recommendations
  - Request Body:
    ```json
    {
        "prompt": "relaxing jazz for studying",
        "playlist_name": "Study Jazz"
    }
    ```
  - Response:
    ```json
    {
        "status": "success",
        "message": "Playlist created successfully",
        "playlist_id": "spotify_playlist_id"
    }
    ```

### User Operations
- `GET /user/info`
  - Retrieves current user's Spotify information
  - Response:
    ```json
    {
        "id": "user_id",
        "display_name": "User Name",
        "email": "user@example.com",
        "country": "US",
        "product": "premium",
        "followers": {
            "total": 123
        },
        "images": [
            {
                "url": "profile_image_url",
                "height": 300,
                "width": 300
            }
        ]
    }
    ```

- `GET /user/playlists`
  - Retrieves user's Spotify playlists
  - Response:
    ```json
    {
        "items": [
            {
                "id": "playlist_id",
                "name": "Playlist Name",
                "description": "Playlist Description",
                "tracks": {
                    "total": 50
                },
                "public": true
            }
        ],
        "total": 10
    }
    ```

### Error Responses
All endpoints may return the following error responses:

- Authentication Error (401):
  ```json
  {
      "error": "Authentication failed",
      "message": "Invalid or expired token"
  }
  ```

- Not Found Error (404):
  ```json
  {
      "error": "Resource not found",
      "message": "The requested resource could not be found"
  }
  ```

- Server Error (500):
  ```json
  {
      "error": "Internal server error",
      "message": "An unexpected error occurred"
  }
  ```

### Rate Limiting
- The API is rate-limited to 100 requests per hour per user
- Rate limit headers are included in responses:
  ```
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1636238400
  ```

### User Operations
- `GET /user/info`
  - Retrieves current user's Spotify information

## Testing

The project includes comprehensive unit tests for all components. Test structure:

```
tests/
├── conftest.py                 # Shared fixtures
├── test_models/               # Data model tests
│   ├── test_song.py
│   ├── test_songs.py
│   └── test_chart_tags.py
└── test_services/             # Service layer tests
    ├── test_scraper.py
    ├── test_playlist_manager.py
    ├── test_gpt_operations.py
    └── spotify_operations/
        ├── test_spotify_auth.py
        ├── test_spotify_playlist_maker.py
        └── test_user_info_viewer.py
```

### Running Tests
```bash
# Run all tests with coverage
make test-coverage

# Generate HTML coverage report
make test-report
```

## Sample Runs

### Creating Billboard Hot 100 Playlist
![Screenshot 2024-11-06 at 11 08 18 PM](https://github.com/user-attachments/assets/5173a5c8-b602-4654-b1c6-37c90b797aa6)

### Testing Coverage Report
```plaintext
============================= test session starts ==============================
platform darwin -- Python 3.9.7, pytest-7.4.3, pluggy-1.3.0
rootdir: /path/to/project
plugins: hypothesis-6.75.3, cov-4.1.0, reportlog-0.3.0, timeout-2.1.0
collected 47 items

tests/test_models/test_song.py ....                                    [  8%]
tests/test_models/test_songs.py .....                                  [ 19%]
tests/test_models/test_chart_tags.py .....                            [ 29%]
tests/test_services/test_scraper.py .....                             [ 40%]
tests/test_services/test_playlist_manager.py ....                      [ 48%]
tests/test_services/test_gpt_operations.py ....                       [ 57%]
tests/test_services/spotify_operations/test_spotify_auth.py ....       [ 65%]
tests/test_services/spotify_operations/test_spotify_playlist_maker.py ..... [ 76%]
tests/test_services/spotify_operations/test_user_info_viewer.py ....   [ 85%]

----------- coverage: platform darwin, python 3.9.7-final-0 -----------
Name                                                    Stmts   Miss  Cover
-------------------------------------------------------------------------
src/model/chart_tags.py                                   15      0   100%
src/model/song.py                                        12      0   100%
src/model/songs.py                                       18      0   100%
...
-------------------------------------------------------------------------
TOTAL                                                    437     12    97%
```

## Contributing
1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
