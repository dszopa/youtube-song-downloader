#!/usr/bin/env python

from apiclient.discovery import build
import json
import urllib
import unicodedata
import sys
import os

class songDownloader(object):
  """Program Usage:
        Switches:
          --help
              Display the help screen
          --editSaveDirectory <Path>
              Change the download directory to <Path>
          --usePrevDirectory
              Revert the download directory to the previous directory
        Commands:
          python downloadSong.py Artist Name - Song Name Minutes:Seconds
              Download Song By Query and Duration.
          python downloadSong.py Artist Name - Song Name
              Download Song by Query.
  """
  def __init__(self):
    self.DEVELOPER_KEY = "AIzaSyAwF1yzv2ZA2kvKCOs0sRkYeXs5NnKDIFA"
    self.YOUTUBE_API_SERVICE_NAME = "youtube"
    self.YOUTUBE_API_VERSION = "v3"

    with open('settings.json', 'r') as data_file:    
        self.settings = json.load(data_file)

  def printUsage(self):  
    print "Program Usage:"
    print "  Switches:"
    print "\t--help"
    print "\t\tDisplay the help screen"
    print "\t--editSaveDirectory <Path>"
    print "\t\tChange the download directory to <Path>"
    print "\t--usePrevDirectory"
    print "\t\tRevert the download directory to the previous directory"
    print "  Commands:"
    print "\tpython downloadSong.py \"Artist Name - Song Name\" \"Minutes:Seconds\""
    print "\t\tDownload Song By Query and Duration."
    print "\tpython downloadSong.py \"Artist Name - Song Name\""
    print "\t\tDownload Song by Query."

  def verifyNoDuplicateSong(self, query):
    os.chdir(self.settings["saveDirectory"])
    filesInDirectory = os.listdir(os.getcwd())
    for fileName in filesInDirectory:
      if fileName == query + ".mp3":
        print "The desired song \"" + query + ".mp3\" already exists in the directory"
        sys.exit(-1)

  def verifySearchResults(self, search_response):
      if len(search_response.get("items", [])) == 0:
        print "There were no results for the specified song, are you sure you entered it correctly?"
        sys.exit(0)

  def editDownloadLocation(self, path):
    self.settings["previousDirectory"] = self.settings["saveDirectory"]
    self.settings["saveDirectory"] = path
    with open("settings.json", "w") as jsonFile:
      jsonFile.write(json.dumps(self.settings, sort_keys=True, indent=4))

  def usePrevDirectory(self):
    self.settings["saveDirectory"] = self.settings["previousDirectory"]
    with open("settings.json", "w") as jsonFile:
      jsonFile.write(json.dumps(self.settings, sort_keys=True, indent=4))
    print "The download location was changed to: " + self.settings["previousDirectory"]

  def downloadSongByQuery(self):
    query = sys.argv[1]

    self.verifyNoDuplicateSong(query)

    youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
      developerKey=self.DEVELOPER_KEY)

    search_response = youtube.search().list(
      q=query,
      part="id,snippet",
      maxResults=10
    ).execute()

    self.verifySearchResults(search_response)

    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        print "Attempting to download video: https://www.youtube.com/watch?v=" + search_result["id"]["videoId"]
        os.system("youtube-dl --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=" + search_result["id"]["videoId"])
        print "Renaming file to: " + query + ".mp3"
        print "File was saved in: " + self.settings["saveDirectory"]
        if "\"" in search_result["snippet"]["title"]:
          temp =search_result["snippet"]["title"].replace("\"", "\'")
          os.rename(temp + "-" + search_result["id"]["videoId"] + ".mp3", query + ".mp3")
        else:
          os.rename(search_result["snippet"]["title"] + "-" + search_result["id"]["videoId"] + ".mp3", query + ".mp3")
        sys.exit(0)

    print "No song with the specified duration +/- 5 seconds was found, are you sure you entered it correctly?"

  def downloadSongByQueryAndDuration(self):
    query = sys.argv[1]
    givenDuration = map(int, sys.argv[2].split(":"))
    givenDuration = givenDuration[0] * 60 + givenDuration[1]

    self.verifyNoDuplicateSong(query)

    youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
      developerKey=self.DEVELOPER_KEY)

    search_response = youtube.search().list(
      q=query,
      part="id,snippet",
      maxResults=10
    ).execute()

    self.verifySearchResults(search_response)

    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        searchUrl = "https://www.googleapis.com/youtube/v3/videos?id="+search_result["id"]["videoId"]+"&key="+self.DEVELOPER_KEY+"&part=contentDetails"
        response = urllib.urlopen(searchUrl).read()
        data = json.loads(response)
        all_data = data['items']
        contentDetails = all_data[0]['contentDetails']
        duration = map(int, str(contentDetails['duration'])[2:][:-1].split("M"))

        if len(duration) > 1:
          duration = duration[0] * 60 + duration[1]
        else:
          if givenDuration < 60:
              duration = duration[1]
          else:
             duration = duration[0] * 60

        if duration - givenDuration < 5 and duration - givenDuration > -5:
          print "Attempting to download video: https://www.youtube.com/watch?v=" + search_result["id"]["videoId"]
          os.system("youtube-dl --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=" + search_result["id"]["videoId"])
          print "Renaming file to: " + query + ".mp3"
          print "File was saved in: " + self.settings["saveDirectory"]
          if "\"" in search_result["snippet"]["title"]:
            temp =search_result["snippet"]["title"].replace("\"", "\'")
            os.rename(temp + "-" + search_result["id"]["videoId"] + ".mp3", query + ".mp3")
          else:
            os.rename(search_result["snippet"]["title"] + "-" + search_result["id"]["videoId"] + ".mp3", query + ".mp3")
          sys.exit(0)

    print "No song with the specified duration +/- 5 seconds was found, are you sure you entered it correctly?"

# Program Logic
arguments = iter(sys.argv)
songDownloader = songDownloader()
for arg in arguments:
  if arg == "--help":
    songDownloader.printUsage()
    sys.exit(0)
  if arg == "--editSaveDirectory":
    path = arguments.next()
    songDownloader.editDownloadLocation(path)
    print "The download location was changed to: " + path
    sys.exit(0)
  if arg == "--usePrevDirectory":
    songDownloader.usePrevDirectory()
    sys.exit(0)

if len(sys.argv) == 2:
  songDownloader.downloadSongByQuery()
elif len(sys.argv) == 3:
  songDownloader.downloadSongByQueryAndDuration()
else:
  print "There were " + str(len(sys.argv)) + " arguments given when 2 or 3 were expected"
  songDownloader.printUsage()
  sys.exit(-1)