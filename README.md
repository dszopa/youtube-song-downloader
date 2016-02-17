## Installation

youtube-song-downloader requires that python is installed as well as ffmpeg.

Once python and ffmpeg are installed you can setup youtube-song-downloader with the command: 
```python setup.py```

## Usage
Search for song to download with a query and duration:

```python downloadSong.py "Artist Name - Song Name" "Minutes:Seconds"```

Search and download the first song from a given query:

```python downloadSong.py "Artist Name - Song Name"```

To update the directory which files are saved to use the command:

```python downloadSong.py --editSaveDirectory "Path to directory"```

## License

This project is under the MIT License