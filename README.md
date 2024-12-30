
<h1 align="center" style="font-weight: bold;">YTMUSICAPI-FLASK 💻</h1>

<p align="center">
  <a href="#tech">Technologies</a>
  <a href="#started">Getting Started</a>
  <a href="#routes">API Endpoints</a>
  <a href="#contribute">Contribute</a>
</p>


<p align="center">Simple description of what your project do or how to use it</p>


<p align="center">
<a href="https://github.com/reddevil212/flask-hello-world/">📱 Visit this Project</a>
</p>

---
<h2 id="technologies">💻 Technologies</h2>

- Python
- Flask
- yt-dlp (for audio extraction)
- yt-music-api (for YouTube Music data)
- Requests
- Werkzeug (for file handling)
---

<h2 id="started">🚀 Getting started</h2>

This API allows you to fetch audio URLs, search for songs, get artist details, and more. Here's how to set it up locally.

<h3>Prerequisites</h3>

Here you list all prerequisites necessary for running your project. For example:

- [Python 3.x](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- [Git](https://git-scm.com/)


<h3>Cloning</h3>

How to clone your project

```bash
git clone https://github.com/reddevil212/flask-hello-world
```

<h3>Installing Dependencies</h3>

How to Install Dependencies

```bash
#on the project root run this
pip install -r requirements.txt
```

<h3>Starting</h3>

How to start your project

```bash
cd api
python index.py
```

<h2 id="routes">📍 API Endpoints</h2>

Here you can list the main routes of your API, and what are their expected request bodies.
​
| route               | description                                          
|----------------------|-----------------------------------------------------
| <kbd>GET /</kbd>     | Health check to confirm the API is running
| <kbd>POST /get_audio</kbd>     | Retrieves audio download URLs for YouTube videos
| <kbd>GET /search</kbd>     | Search for songs, artists, or albums
| <kbd>GET /search_suggestions</kbd>     | Get search suggestions based on query
| <kbd>GET /get_artist</kbd>     | Retrieve information about a specific artist
| <kbd>GET /artists/{artist_id}/albums</kbd>     | Get albums of a specific artist
| <kbd>GET /songs/{song_id}</kbd>     | Retrieve details of a specific song
| <kbd>GET /songs/{song_id}/related</kbd>     | Retrieve related songs for a given song

<h3 id="response1">📋 Example Requests</h3>
**POST /get_audio**
**Request**
```json
{
  "urls": ["https://youtube.com/watch?v=dQw4w9WgXcQ"],
  "cookies_url": "https://example.com/cookies.txt"
}
```

**Response**
```json
{
  "urls": [
    {
      "value": 1,
      "audio_url": "https://audio-stream-url.com/audio.mp4"
    }
  ]
}
```

**GET /search**
**Request**
```json
{
GET /search?query=Beatles

}
```

**Response**
```json
{
  "results": [
    {
      "title": "Hey Jude",
      "artist": "The Beatles",
      "album": "Revolution"
    },
    {
      "title": "Let It Be",
      "artist": "The Beatles",
      "album": "Let It Be"
    }
  ]
}
```


<h2 id="contribute">📫 Contribute</h2>

Feel free to contribute to this project! Here’s how you can help:

1. Fork the repository: ```git fork https://github.com/reddevil212/flask-hello-world```
2. Create a new branch: ```git checkout -b feature/feature-name```
3. Make your changes and commit them: ```git commit -m "Add feature"```
4. Push your changes: ```git push origin feature/feature-name```
5. Create a Pull Request (PR) and describe what you've done.


<h3>Documentations that might help</h3>

[💾 ytmusicapi](https://github.com/sigma67/ytmusicapi)
[📝 How to create a Pull Request](https://www.atlassian.com/br/git/tutorials/making-a-pull-request)

[💾 Commit pattern](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)



