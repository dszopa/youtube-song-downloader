## Installation

youtube-song-downloader requires that Python 2.7 is installed as well as ffmpeg.

You can install youtube-song-downloader with pip using:

```pip install youtube-song-downloader```

or with setup.py from the repository using the command:

```python setup.py install```


## Usage
Search for song to download with a search query and duration (Default is +/- 5 seconds):

```youtube-song-downloader "Artist Name - Song Name" "Minutes:Seconds"```

Search and download the first song from a given search query:

```youtube-song-downloader "Artist Name - Song Name"```

To download a song with the exact duration use:

```youtube-song-downloader --exact "Artist Name - Song Name" "Minutes:Seconds"```

To specify the buffer (in seconds) on the duration of the song use:

```youtube-song-downloader --buffer <Buffer> "Artist Name - Song Name" "Min:Sec"```

To download a song by link:

```youtube-song-downloader --link <Youtube URL>```

To update the directory which files are saved to use the command:

```youtube-song-downloader --changeSaveDir "Path to directory"```

To use the previous directory use the command:

```youtube-song-downloader --usePrevDir```


## License

This project is under the MIT License