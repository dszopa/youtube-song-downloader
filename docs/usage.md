## Installation

youtube-song-downloader requires that python is installed as well as ffmpeg.

Once python and ffmpeg are installed you can setup youtube-song-downloader with the command: 
```python setup.py```

## Usage
Search for song to download with a search query and duration (Default is +/- 5 seconds):

```python youtube-song-downloader.py "Artist Name - Song Name" "Minutes:Seconds"```

Search and download the first song from a given search query:

```python youtube-song-downloader.py "Artist Name - Song Name"```

To download a song by link:

```python youtube-song-downloader.py --link <Youtube URL>```

To update the directory which files are saved to use the command:

```python youtube-song-downloader.py --editSaveDirectory "Path to directory"```

To download a song with the exact duration use:

```python youtube-song-downloader.py --exact "Artist Name - Song Name" "Minutes:Seconds"```

To specify the buffer on the duration of the song use:

```python youtube-song-downloader.py --buffer <Buffer In Seconds> "Artist Name - Song Name" "Minutes:Seconds"```