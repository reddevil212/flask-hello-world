import os
import yt_dlp
import tempfile
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import aiohttp
import asyncio

app = Flask(__name__)

# Configure a temporary directory for storing uploaded files
TEMP_DIR = tempfile.mkdtemp()

# Default cookies file URL if no cookies file or cookies URL is provided
DEFAULT_COOKIES_URL = "https://raw.githubusercontent.com/reddevil212/jks/refs/heads/main/cookies.txt"
COOKIES_CACHE_PATH = os.path.join(TEMP_DIR, 'cookies_cache.txt')
COOKIE_EXPIRATION_TIME = 3600  # Cache cookies for 1 hour

# Helper function to validate YouTube URL
def is_valid_youtube_url(url):
    return 'youtube.com' in url or 'youtu.be' in url

# Cache check for cookies
def get_cached_cookies():
    if os.path.exists(COOKIES_CACHE_PATH):
        file_age = time.time() - os.path.getmtime(COOKIES_CACHE_PATH)
        if file_age < COOKIE_EXPIRATION_TIME:
            return COOKIES_CACHE_PATH
    return None

# Download cookies from URL
async def download_cookies_from_url(url, download_path):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                content = await response.read()
                with open(download_path, 'wb') as f:
                    f.write(content)
            return download_path
        except Exception as e:
            print(f"Error downloading cookies: {str(e)}")
            return None

# Get audio URL from YouTube video
def get_audio_url_from_json(video_url, cookies_file_path):
    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'quiet': True,
        'cookiefile': cookies_file_path,
        'forcejson': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(video_url, download=False)
            for format in info_dict['formats']:
                if format['acodec'] == 'opus' and format['vcodec'] == 'none' and format.get('url'):
                    return format['url']
            return None
        except Exception as e:
            print(f"Error extracting audio URL: {str(e)}")
            return None

# Optimized function to process each video URL asynchronously
def get_audio_for_video(video_url, cookies_file_path):
    try:
        audio_url = get_audio_url_from_json(video_url, cookies_file_path)
        if audio_url:
            return {'audio_url': audio_url}
        else:
            return {'audio_url': 'Audio stream not found'}
    except Exception as e:
        return {'audio_url': f"Error: {str(e)}"}

# Main endpoint for fetching audio
@app.route('/get_audio', methods=['POST'])
def get_audio():
    # Check if JSON data is provided
    if request.is_json:
        data = request.get_json()
        video_urls = data.get('urls', [])
        cookies_url = data.get('cookies_url', None)
    else:
        video_urls = request.form.getlist('urls[]')
        cookies_url = request.form.get('cookies_url', None)

    # Validate URLs
    if not video_urls:
        return jsonify({'error': 'No YouTube URLs provided'}), 400

    # Handling cookies - check for cached or default cookies
    cookies_file_path = get_cached_cookies()
    if not cookies_file_path:
        if cookies_url:
            cookies_file_path = os.path.join(TEMP_DIR, 'cookies.txt')
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(download_cookies_from_url(cookies_url, cookies_file_path))
            if result is None:
                return jsonify({'error': 'Failed to download cookies'}), 400
        else:
            cookies_file_path = os.path.join(TEMP_DIR, 'cookies.txt')
            result = asyncio.run(download_cookies_from_url(DEFAULT_COOKIES_URL, cookies_file_path))
            if result is None:
                return jsonify({'error': 'Failed to download default cookies'}), 400

        # Cache the downloaded cookies
        if cookies_file_path:
            with open(COOKIES_CACHE_PATH, 'wb') as f:
                with open(cookies_file_path, 'rb') as original:
                    f.write(original.read())

    # Validate YouTube URLs
    invalid_urls = [url for url in video_urls if not is_valid_youtube_url(url)]
    valid_urls = [url for url in video_urls if is_valid_youtube_url(url)]

    if invalid_urls:
        return jsonify({'error': 'Invalid YouTube URLs', 'invalid_urls': invalid_urls}), 400

    # Process valid URLs in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(get_audio_for_video, url, cookies_file_path): url for url in valid_urls}
        urls_data = []
        for future in as_completed(future_to_url):
            result = future.result()
            urls_data.append(result)

    # Return the results
    return jsonify({'urls': urls_data})

# Health check endpoint
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "success", "message": "The API is up and running!"}), 200

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
