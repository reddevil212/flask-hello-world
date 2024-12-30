# YouTube Music API

This is a Flask-based API that integrates with `ytmusicapi` and `yt-dlp` to provide music-related functionalities such as searching for songs, retrieving artist and album information, and fetching audio URLs from YouTube videos. It is designed to be used for applications that need to interact with YouTube Music and YouTube videos to extract media data.

## Features

- **Search for Songs, Artists, and Albums** on YouTube Music.
- **Retrieve Artist Information** based on artist ID.
- **Fetch Audio URL** for YouTube videos using yt-dlp.
- **Get Related Songs** for a given song ID.
- **Health Check** to verify if the API is up and running.
- **Retrieve Detailed Album Information** and browse IDs.
- **Custom Cookie Management** for YouTube video downloads.

## Endpoints

### 1. `/get_audio` (POST)

Fetches the best audio URL for a list of YouTube video URLs.

#### Request

- **Method**: `POST`
- **Content-Type**: `application/json` or `multipart/form-data`
- **Body**:
  - `urls[]`: List of YouTube video URLs to extract audio from (required).
  - `cookies_url` (optional): URL to a `cookies.txt` file for authentication.
  - Alternatively, you can upload a `cookies.txt` file directly.

#### Example Request:

```json
{
  "urls": [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://youtu.be/dQw4w9WgXcQ"
  ],
  "cookies_url": "https://example.com/cookies.txt"
}
