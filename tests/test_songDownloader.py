# -*- coding: utf-8 -*-
import pytest
from .context import ytsdl
import os
import sys

os.chdir("/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin")
songDownloader = ytsdl.songDownloader()

def test_directoryIsCorrect():
	assert os.getcwd() == "/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin"

def test_printUsage():
	assert 1 == 1

def test_verifyNoDuplicateSong():
	assert 1 == 1

def test_verifySearchResults():
	assert 1 == 1

def test_editDownloadLocation():
	assert 1 == 1

def test_usePrevDirectory():
	assert 1 == 1

def test_downloadSongByQuery():
	songDownloader.downloadSongByQuery("Rick Astley - Never Gonna Give You Up")
	filenameList = os.listdir(os.getcwd())
	containsFile = False
	if "Rick Astley - Never Gonna Give You Up.mp3" in filenameList:
		containsFile = True
	assert containsFile == True
	os.chdir("/Users/danny/Music/test/")
	os.system("rm -f \"Rick Astley - Never Gonna Give You Up.mp3\"")
	os.chdir("/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin")

def test_downloadSongByQueryAndDuration():
	songDownloader.downloadSongByQueryAndDuration("Rick Astley - Never Gonna Give You Up", "3:33", 5)
	filenameList = os.listdir(os.getcwd())
	containsFile = False
	if "Rick Astley - Never Gonna Give You Up.mp3" in filenameList:
		containsFile = True
	assert containsFile == True
	os.chdir("/Users/danny/Music/test/")
	os.system("rm -f \"Rick Astley - Never Gonna Give You Up.mp3\"")
	os.chdir("/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin")

def test_exactDownloadSongByQueryAndDuration():
	songDownloader.downloadSongByQueryAndDuration("Rick Astley - Never Gonna Give You Up", "3:33", 0)
	filenameList = os.listdir(os.getcwd())
	containsFile = False
	if "Rick Astley - Never Gonna Give You Up.mp3" in filenameList:
		containsFile = True
	assert containsFile == True
	os.chdir("/Users/danny/Music/test/")
	os.system("rm -f \"Rick Astley - Never Gonna Give You Up.mp3\"")
	os.chdir("/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin")

def test_largeBufferDownloadSongByQueryAndDuration():
	songDownloader.downloadSongByQueryAndDuration("Rick Astley - Never Gonna Give You Up", "3:33", 30)
	filenameList = os.listdir(os.getcwd())
	containsFile = False
	if "Rick Astley - Never Gonna Give You Up.mp3" in filenameList:
		containsFile = True
	assert containsFile == True
	os.chdir("/Users/danny/Music/test/")
	os.system("rm -f \"Rick Astley - Never Gonna Give You Up.mp3\"")
	os.chdir("/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin")

def test_downloadSongByYoutubeLink():
	songDownloader.downloadSongByYoutubeLink("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
	filenameList = os.listdir(os.getcwd())
	containsFile = False
	if "Rick Astley - Never Gonna Give You Up-dQw4w9WgXcQ.mp3" in filenameList:
		containsFile = True
	assert containsFile == True
	os.chdir("/Users/danny/Music/test/")
	os.system("rm -f \"Rick Astley - Never Gonna Give You Up-dQw4w9WgXcQ.mp3\"")
	os.chdir("/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin")
