import json
import time
import logging
from typing import List, Dict, Any, Optional
import openai
from tenacity import retry, stop_after_attempt, wait_exponential
from model.song import Song
from model.songs import Songs
from config import Config

class GPTOperations:
    LOG_PREFIX = "[GPTOperations]"

    def __init__(self):
        """Initialize GPT Operations with enhanced configuration."""
        config = Config()
        self.api_key = config.get_gpt_key()
        openai.api_key = self.api_key
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Rate limiting configuration
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum time between requests in seconds
        
        # Cost management
        self.total_tokens_used = 0
        self.budget_limit = 100000  # Maximum tokens to use before warning
        
        # Response quality configuration
        self.min_songs_required = 5
        self.max_songs_allowed = 30
        self.max_prompt_length = 500
        
        self.logger.info(f"{self.LOG_PREFIX} GPTOperations initialized successfully")

    def _check_rate_limit(self):
        """Implement rate limiting between API calls."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            self.logger.debug(f"{self.LOG_PREFIX} Rate limiting active: Waiting {sleep_time:.2f} seconds before next request")
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def _validate_prompt(self, prompt: str) -> tuple[bool, str]:
        """
        Validate and sanitize the input prompt.
        """
        if not prompt or not isinstance(prompt, str):
            self.logger.error(f"{self.LOG_PREFIX} Prompt validation failed: Empty or invalid input type")
            return False, "Prompt must be a non-empty string"
        
        if len(prompt) > self.max_prompt_length:
            self.logger.error(f"{self.LOG_PREFIX} Prompt validation failed: Length {len(prompt)} exceeds limit {self.max_prompt_length}")
            return False, f"Prompt exceeds maximum length of {self.max_prompt_length} characters"
        
        # Basic sanitization
        sanitized_prompt = prompt.strip()
        sanitized_prompt = ' '.join(sanitized_prompt.split())  # Normalize whitespace
        
        if not sanitized_prompt:
            self.logger.error(f"{self.LOG_PREFIX} Prompt validation failed: Empty content after sanitization")
            return False, "Prompt contains no valid content after sanitization"
            
        self.logger.debug(f"{self.LOG_PREFIX} Prompt validation successful: {sanitized_prompt[:50]}...")
        return True, sanitized_prompt

    def _track_token_usage(self, response: Any):
        """Track token usage and log warnings if approaching limits."""
        if hasattr(response, 'usage'):
            tokens_used = response.usage.total_tokens
            self.total_tokens_used += tokens_used
            
            self.logger.info(f"{self.LOG_PREFIX} Request token usage: {tokens_used} | Total usage: {self.total_tokens_used}")
            
            usage_percentage = (self.total_tokens_used / self.budget_limit) * 100
            if usage_percentage > 80:
                self.logger.warning(f"{self.LOG_PREFIX} Token usage alert: {usage_percentage:.1f}% of budget consumed")
            elif usage_percentage > 60:
                self.logger.info(f"{self.LOG_PREFIX} Token usage status: {usage_percentage:.1f}% of budget consumed")

    def _validate_response_quality(self, songs: List[Dict[str, str]]) -> tuple[bool, str]:
        """
        Validate the quality of the response.
        """
        if not songs:
            self.logger.error(f"{self.LOG_PREFIX} Response quality check failed: Empty response")
            return False, "No songs returned in response"
            
        if len(songs) < self.min_songs_required:
            self.logger.error(f"{self.LOG_PREFIX} Response quality check failed: Only {len(songs)} songs returned")
            return False, f"Response contains fewer than {self.min_songs_required} songs"
            
        if len(songs) > self.max_songs_allowed:
            self.logger.error(f"{self.LOG_PREFIX} Response quality check failed: Excessive songs ({len(songs)})")
            return False, f"Response contains more than {self.max_songs_allowed} songs"
            
        # Check for duplicates
        seen_songs = set()
        for song in songs:
            song_key = f"{song.get('title', '').lower()}|{song.get('artist', '').lower()}"
            if song_key in seen_songs:
                self.logger.error(f"{self.LOG_PREFIX} Response quality check failed: Duplicate song found - {song}")
                return False, "Response contains duplicate songs"
            seen_songs.add(song_key)
            
        self.logger.info(f"{self.LOG_PREFIX} Response quality check passed: {len(songs)} valid songs")
        return True, "Response quality checks passed"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def fetch_songs(self, prompt: str) -> Songs:
        """
        Fetch songs based on the user's prompt using GPT-4 with enhanced error handling and validation.
        """
        try:
            self.logger.info(f"{self.LOG_PREFIX} Starting song fetch process for prompt: '{prompt[:50]}...'")
            
            # Input validation
            is_valid, result = self._validate_prompt(prompt)
            if not is_valid:
                self.logger.error(f"{self.LOG_PREFIX} Prompt validation failed: {result}")
                return Songs([])
                
            sanitized_prompt = result
            
            # Rate limiting
            self._check_rate_limit()
            
            # Make API call
            self.logger.info(f"{self.LOG_PREFIX} Initiating GPT API call")
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You MUST return an array of AT LEAST 5 songs matching the query. "
                                 "Response must be a JSON array with multiple objects. Each object must "
                                 "only have title and artist fields. Format: "
                                 "[{\"title\": \"Hey Jude\", \"artist\": \"The Beatles\"}, "
                                 "{\"title\": \"Let It Be\", \"artist\": \"The Beatles\"}]. "
                                 "Always return minimum 20 songs in array format."
                    },
                    {
                        "role": "user",
                        "content": sanitized_prompt
                    }
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            self.logger.info(f"{self.LOG_PREFIX} API call completed successfully")
            
            # Track token usage
            self._track_token_usage(response)
            
            # Parse response
            content = response.choices[0].message.content
            data = json.loads(content)
            songs_data = data.get('songs', [])
            
            # Validate response quality
            is_valid, quality_message = self._validate_response_quality(songs_data)
            if not is_valid:
                self.logger.error(f"{self.LOG_PREFIX} Quality validation failed: {quality_message}")
                return Songs([])
            
            # Convert to Song objects
            songs_list = []
            for idx, song_data in enumerate(songs_data, 1):
                if self.validate_song(song_data):
                    songs_list.append(Song(
                        title=song_data['title'],
                        artist=song_data['artist']
                    ))
                    self.logger.debug(f"{self.LOG_PREFIX} Processed song {idx}: {song_data['title']} by {song_data['artist']}")
            
            self.logger.info(f"{self.LOG_PREFIX} Successfully processed {len(songs_list)} songs")
            return Songs(songs_list)
            
        except openai.error.RateLimitError:
            self.logger.error(f"{self.LOG_PREFIX} API rate limit exceeded")
            raise
        except openai.error.APIError as e:
            self.logger.error(f"{self.LOG_PREFIX} OpenAI API error occurred: {str(e)}")
            raise
        except json.JSONDecodeError:
            self.logger.error(f"{self.LOG_PREFIX} Failed to parse API response as JSON")
            return Songs([])
        except Exception as e:
            self.logger.error(f"{self.LOG_PREFIX} Unexpected error in fetch_songs: {str(e)}", exc_info=True)
            return Songs([])

    def validate_song(self, song: Dict[str, Any]) -> bool:
        """
        Validate that a song dictionary has the required fields.
        """
        try:
            is_valid = (
                isinstance(song, dict) and
                'title' in song and
                'artist' in song and
                isinstance(song['title'], str) and
                isinstance(song['artist'], str) and
                len(song['title'].strip()) > 0 and
                len(song['artist'].strip()) > 0
            )
            
            if not is_valid:
                self.logger.warning(f"{self.LOG_PREFIX} Invalid song data structure: {song}")
            
            return is_valid
            
        except Exception as e:
            self.logger.error(f"{self.LOG_PREFIX} Error validating song data: {str(e)}")
            return False

    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get current usage statistics.
        """
        stats = {
            "total_tokens_used": self.total_tokens_used,
            "budget_limit": self.budget_limit,
            "budget_percentage": (self.total_tokens_used / self.budget_limit) * 100
        }
        
        self.logger.info(f"{self.LOG_PREFIX} Current usage stats - {stats['budget_percentage']:.1f}% of budget consumed")
        return stats