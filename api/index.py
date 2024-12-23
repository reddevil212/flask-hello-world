import os
import yt_dlp
import tempfile
import requests
import time
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure a temporary directory for storing uploaded files
TEMP_DIR = tempfile.mkdtemp()

# Default cookies file URL if no cookies file or cookies URL is provided
DEFAULT_COOKIES_URL = "https://raw.githubusercontent.com/reddevil212/jks/refs/heads/main/cookies.txt"

# Helper function to validate YouTube URL
def is_valid_youtube_url(url):
    return 'youtube.com' in url or 'youtu.be' in url

# Helper function to download cookies file from URL
def download_cookies_from_url(url, download_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        with open(download_path, 'wb') as f:
            f.write(response.content)
        return download_path
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to download cookies: {str(e)}"}

# Function to extract the best audio URL from a YouTube video using yt-dlp
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
        except Exception as e:
            return None

# Centralized function for handling the cookie retrieval logic
def handle_cookies(request, cookies_url):
    cookies_file_path = None
    cookies_file = request.files.get('cookies.txt')
    
    if cookies_file:
        cookies_file_path = os.path.join(TEMP_DIR, secure_filename(cookies_file.filename))
        cookies_file.save(cookies_file_path)
    elif cookies_url:
        cookies_file_path = os.path.join(TEMP_DIR, 'cookies.txt')
        result = download_cookies_from_url(cookies_url, cookies_file_path)
        if isinstance(result, dict) and 'error' in result:
            return result
    else:
        cookies_file_path = os.path.join(TEMP_DIR, 'cookies.txt')
        result = download_cookies_from_url(DEFAULT_COOKIES_URL, cookies_file_path)
        if isinstance(result, dict) and 'error' in result:
            return result
    
    return cookies_file_path

# Route to fetch the audio download URL for multiple URLs
@app.route('/get_audio', methods=['POST'])
def get_audio():
    if request.is_json:
        data = request.get_json()
        video_urls = data.get('urls', [])
        cookies_url = data.get('cookies_url', None)
    else:
        video_urls = request.form.getlist('urls[]')
        cookies_url = request.form.get('cookies_url', None)

    if not video_urls:
        return jsonify({'error': 'No YouTube URLs provided'}), 400

    # Handle cookies
    cookies_file_path = handle_cookies(request, cookies_url)
    if isinstance(cookies_file_path, dict) and 'error' in cookies_file_path:
        return jsonify(cookies_file_path), 400

    # Validate video URLs
    valid_urls = [url for url in video_urls if is_valid_youtube_url(url)]
    invalid_urls = [url for url in video_urls if not is_valid_youtube_url(url)]

    if invalid_urls:
        return jsonify({'error': 'Invalid YouTube URLs', 'invalid_urls': invalid_urls}), 400

    # Fetch audio URLs for valid video URLs
    urls_data = []
    for idx, video_url in enumerate(valid_urls, 1):
        audio_url = get_audio_url_from_json(video_url, cookies_file_path)
        if audio_url:
            urls_data.append({'value': idx, 'audio_url': audio_url})
        else:
            urls_data.append({'value': idx, 'audio_url': 'Audio stream not found'})

    return jsonify({'urls': urls_data})


# Endpoint to search for songs, artists, and albums
@app.route('/search', methods=['GET'])
def search():
    start_time = time.time()  # Start measuring time
    query = request.args.get('query')
    results = ytmusic.search(query)
    end_time = time.time()  # End measuring time
    print(f"Search Request Time: {end_time - start_time:.4f} seconds")  # Print time taken
    return jsonify(results)

@app.route('/search_suggestions', methods=['GET'])
def search_suggestions():
    start_time = time.time()  # Start measuring time
    query = request.args.get('query')
    detailed_runs = request.args.get('detailed_runs', default=False, type=lambda x: (x.lower() == 'true'))

    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    try:
        suggestions = ytmusic.get_search_suggestions(query, detailed_runs)
        end_time = time.time()  # End measuring time
        print(f"Search Suggestions Request Time: {end_time - start_time:.4f} seconds")  # Print time taken
        return jsonify(suggestions)
    except Exception as e:
        end_time = time.time()  # End measuring time
        print(f"Search Suggestions Error Time: {end_time - start_time:.4f} seconds")  # Print time taken on error
        return jsonify({'error': str(e)}), 500

@app.route('/get_artist', methods=['GET'])
def get_artist():
    start_time = time.time()  # Start measuring time
    artist_id = request.args.get('artistId')
    if not artist_id:
        return jsonify({'error': 'Artist ID parameter is required'}), 400

    try:
        artist_info = ytmusic.get_artist(artist_id)
        end_time = time.time()  # End measuring time
        print(f"Get Artist Request Time: {end_time - start_time:.4f} seconds")  # Print time taken
        return jsonify(artist_info)
    except Exception as e:
        end_time = time.time()  # End measuring time
        print(f"Get Artist Error Time: {end_time - start_time:.4f} seconds")  # Print time taken on error
        return jsonify({'error': str(e)}), 500

# Endpoint to retrieve artist albums
@app.route('/artists/<string:artist_id>/albums', methods=['GET'])
def get_artist_albums(artist_id):
    start_time = time.time()  # Start measuring time
    results = ytmusic.get_artist_albums(artist_id)
    end_time = time.time()  # End measuring time
    print(f"Get Artist Albums Time: {end_time - start_time:.4f} seconds")  # Print time taken
    return jsonify(results)

# Endpoint to retrieve album data
@app.route('/albums/<string:album_id>', methods=['GET'])
def get_album(album_id):
    start_time = time.time()  # Start measuring time
    results = ytmusic.get_album(album_id)
    end_time = time.time()  # End measuring time
    print(f"Get Album Request Time: {end_time - start_time:.4f} seconds")  # Print time taken
    return jsonify(results)

# Endpoint to retrieve album browse ID
@app.route('/albums/<string:album_id>/browse_id', methods=['GET'])
def get_album_browse_id(album_id):
    start_time = time.time()  # Start measuring time
    results = ytmusic.get_album_browse_id(album_id)
    end_time = time.time()  # End measuring time
    print(f"Get Album Browse ID Request Time: {end_time - start_time:.4f} seconds")  # Print time taken
    return jsonify(results)

# Endpoint to retrieve song data
@app.route('/songs/<string:song_id>', methods=['GET'])
def get_song(song_id):
    start_time = time.time()  # Start measuring time
    results = ytmusic.get_song(song_id)
    end_time = time.time()  # End measuring time
    print(f"Get Song Request Time: {end_time - start_time:.4f} seconds")  # Print time taken
    return jsonify(results)

# Endpoint to retrieve related songs
@app.route('/songs/<string:song_id>/related', methods=['GET'])
def get_song_related(song_id):
    start_time = time.time()  # Start measuring time
    results = ytmusic.get_song_related(song_id)
    end_time = time.time()  # End measuring time
    print(f"Get Song Related Request Time: {end_time - start_time:.4f} seconds")  # Print time taken
    return jsonify(results)





# Health check endpoint to ensure the server is running
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "success", "message": "The API is up and running!"}), 200

# Start the Flask server
if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
