# -*- coding: utf-8 -*-
import pytest
from .context import ytsdl
from apiclient.discovery import build
import json
import urllib
import unicodedata
import os
import sys

# If any of the downloadSong test fail you most likely have to delete files from the save directory

os.chdir("/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin")
songDownloader = ytsdl.songDownloader()

def test_directoryIsCorrect():
	assert os.getcwd() == "/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin"

def test_verifyNoDuplicateSong():
	os.chdir("/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin")
	open("Test.mp3", 'a')
	duplicateSong = songDownloader.verifyNoDuplicateSong("Test")
	noDuplicateSong = songDownloader.verifyNoDuplicateSong("Noone would ever name their song this")
	os.remove("Test.mp3")
	os.chdir("/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin")

	assert duplicateSong == False
	assert noDuplicateSong == True

def test_verifySearchResults():
	DEVELOPER_KEY = "AIzaSyAwF1yzv2ZA2kvKCOs0sRkYeXs5NnKDIFA"
	YOUTUBE_API_SERVICE_NAME = "youtube"
	YOUTUBE_API_VERSION = "v3"

	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
	developerKey=DEVELOPER_KEY)

	invalid_search_response = youtube.search().list(
	  q="kahsdlfhaslkdjfhalskhjdflkajhsdflkjahsdflkjahsldkfhjaslkfhaklsdjhflkasjhdfklasjhdflkajshdflkajshdflkjashdflkjashdfkljashdklfjahslkdjfhaskljdfh",
	  part="id,snippet",
	  maxResults=10
	).execute()

	valid_search_response = youtube.search().list(
	  q="Tiesto - Secrets",
	  part="id,snippet",
	  maxResults=10
	).execute()

	invalidResults = songDownloader.verifySearchResults(invalid_search_response)
	validResults = songDownloader.verifySearchResults(valid_search_response)

	assert invalidResults == False
	assert validResults == True

def test_editDownloadLocation():
	with open('settings.json', 'r') as data_file:    
		initialSettings = json.load(data_file)

	songDownloader.editDownloadLocation("testLocation")
	songDownloader.editDownloadLocation("testLocation")

	with open('settings.json', 'r') as data_file:
		finalSettings = json.load(data_file)

	finalCurrentDir = finalSettings["saveDirectory"] == "testLocation"
	finalPastDir = finalSettings["previousDirectory"] == "testLocation"

	with open('settings.json', 'w') as jsonFile:
		jsonFile.write(json.dumps(initialSettings, sort_keys=True, indent=4))

	# These are needed because the data is cached in memory for ytsdl.songDownloader()
	songDownloader.editDownloadLocation("/Users/danny/Music/test/")
	songDownloader.editDownloadLocation("/Users/danny/Music/test/")

	assert finalCurrentDir == True
	assert finalPastDir == True

def test_usePrevDirectory():
	with open('settings.json', 'r') as data_file:    
		initialSettings = json.load(data_file)

	songDownloader.editDownloadLocation("previousTestLocation")
	songDownloader.editDownloadLocation("testLocation")
	songDownloader.usePrevDirectory()

	with open('settings.json', 'r') as data_file:
		finalSettings = json.load(data_file)

	finalCurrentDir = finalSettings["saveDirectory"] == "previousTestLocation"
	finalPastDir = finalSettings["previousDirectory"] == "previousTestLocation"

	with open('settings.json', 'w') as jsonFile:
		jsonFile.write(json.dumps(initialSettings, sort_keys=True, indent=4))

	# These are needed because the data is cached in memory for ytsdl.songDownloader()
	songDownloader.editDownloadLocation("/Users/danny/Music/test/")
	songDownloader.editDownloadLocation("/Users/danny/Music/test/")

	assert finalCurrentDir == True
	assert finalPastDir == True

def test_downloadSongByQuery():
	songDownloader.downloadSongByQuery("Rick Astley - Never Gonna Give You Up")
	filenameList = os.listdir(os.getcwd())
	containsFile = False
	if "Rick Astley - Never Gonna Give You Up.mp3" in filenameList:
		containsFile = True
	os.chdir("/Users/danny/Music/test/")
	os.system("rm -f \"Rick Astley - Never Gonna Give You Up.mp3\"")
	os.chdir("/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin")
	assert containsFile == True

def test_downloadSongByQueryAndDuration():
	songDownloader.downloadSongByQueryAndDuration("Rick Astley - Never Gonna Give You Up", "3:33", 5)
	filenameList = os.listdir(os.getcwd())
	containsFile = False
	if "Rick Astley - Never Gonna Give You Up.mp3" in filenameList:
		containsFile = True
	os.chdir("/Users/danny/Music/test/")
	os.system("rm -f \"Rick Astley - Never Gonna Give You Up.mp3\"")
	os.chdir("/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin")
	assert containsFile == True

def test_exactDownloadSongByQueryAndDuration():
	songDownloader.downloadSongByQueryAndDuration("Rick Astley - Never Gonna Give You Up", "3:33", 0)
	filenameList = os.listdir(os.getcwd())
	containsFile = False
	if "Rick Astley - Never Gonna Give You Up.mp3" in filenameList:
		containsFile = True
	os.chdir("/Users/danny/Music/test/")
	os.system("rm -f \"Rick Astley - Never Gonna Give You Up.mp3\"")
	os.chdir("/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin")
	assert containsFile == True

def test_largeBufferDownloadSongByQueryAndDuration():
	songDownloader.downloadSongByQueryAndDuration("Rick Astley - Never Gonna Give You Up", "3:33", 30)
	filenameList = os.listdir(os.getcwd())
	containsFile = False
	if "Rick Astley - Never Gonna Give You Up.mp3" in filenameList:
		containsFile = True
	os.chdir("/Users/danny/Music/test/")
	os.system("rm -f \"Rick Astley - Never Gonna Give You Up.mp3\"")
	os.chdir("/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin")
	assert containsFile == True

def test_downloadSongByYoutubeLink():
	songDownloader.downloadSongByYoutubeLink("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
	filenameList = os.listdir(os.getcwd())
	containsFile = False
	if "Rick Astley - Never Gonna Give You Up-dQw4w9WgXcQ.mp3" in filenameList:
		containsFile = True
	os.chdir("/Users/danny/Music/test/")
	os.system("rm -f \"Rick Astley - Never Gonna Give You Up-dQw4w9WgXcQ.mp3\"")
	os.chdir("/Users/danny/Documents/Coding/Python/youtube-song-downloader/bin")
	assert containsFile == True