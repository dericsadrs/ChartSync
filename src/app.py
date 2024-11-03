from flask import Flask, request, jsonify
from services.playlist_manager import PlaylistManager
from services.gpt_operations import GPTOperations
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "music-playlist-service"})

@app.route('/api/playlists/charts/<chart_type>', methods=['POST'])
def create_chart_playlist(chart_type):
    """Create a playlist based on chart type."""
    try:
        logger.info(f"[PlaylistAPI] Creating playlist for chart type: {chart_type}")
        playlist_manager = PlaylistManager()
        result = playlist_manager.create_playlist(chart_type=chart_type)
        return jsonify(result)
    except Exception as e:
        logger.error(f"[PlaylistAPI] Error creating chart playlist: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/playlists/gpt', methods=['POST'])
def create_gpt_playlist():
    """Create a playlist based on GPT recommendations."""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"status": "error", "message": "Missing prompt in request"}), 400

        prompt = data['prompt']
        playlist_name = data.get('playlist_name', 'GPT Recommended Songs')
        description = data.get('description', 'Playlist created from GPT recommendations')

        logger.info(f"[PlaylistAPI] Creating GPT playlist with prompt: {prompt}")
        
        # Get song recommendations from GPT
        gpt_ops = GPTOperations()
        songs = gpt_ops.fetch_songs(prompt)
        
        if not songs.songs:
            return jsonify({"status": "error", "message": "No songs found for the given prompt"}), 404
            
        # Create playlist with recommended songs
        playlist_manager = PlaylistManager()
        result = playlist_manager.create_playlist_from_songs(
            songs=songs,
            playlist_name=playlist_name,
            description=description
        )
        
        # Get usage statistics
        usage_stats = gpt_ops.get_usage_stats()
        
        return jsonify({
            "status": "success",
            "playlist": result,
            "songs_count": len(songs.songs),
            "usage_stats": usage_stats
        })
        
    except Exception as e:
        logger.error(f"[PlaylistAPI] Error creating GPT playlist: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/recommendations', methods=['POST'])
def get_gpt_recommendations():
    """Get song recommendations without creating a playlist."""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"status": "error", "message": "Missing prompt in request"}), 400

        prompt = data['prompt']
        logger.info(f"[PlaylistAPI] Getting GPT recommendations for prompt: {prompt}")
        
        gpt_ops = GPTOperations()
        songs = gpt_ops.fetch_songs(prompt)
        
        if not songs.songs:
            return jsonify({"status": "error", "message": "No songs found for the given prompt"}), 404
            
        # Convert songs to dictionary format
        songs_list = [{"title": song.title, "artist": song.artist} for song in songs.songs]
        
        return jsonify({
            "status": "success",
            "songs": songs_list,
            "count": len(songs_list)
        })
        
    except Exception as e:
        logger.error(f"[PlaylistAPI] Error getting GPT recommendations: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)