from apiclient.discovery import build
import json
import urllib
import unicodedata
import sys
import os

DEVELOPER_KEY = "AIzaSyAwF1yzv2ZA2kvKCOs0sRkYeXs5NnKDIFA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

with open('settings.json', 'r') as data_file:    
    settings = json.load(data_file)

def printUsage():  
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

def verifyNoDuplicateSong(query):
  os.chdir(settings["saveDirectory"])
  filesInDirectory = os.listdir(os.getcwd())
  for fileName in filesInDirectory:
    if fileName == query + ".mp3":
      print "The desired song \"" + query + ".mp3\" already exists in the directory"
      sys.exit(-1)

def verifySearchResults(search_response):
    if len(search_response.get("items", [])) == 0:
      print "There were no results for the specified song, are you sure you entered it correctly?"
      sys.exit(0)

def editDownloadLocation(path):
  settings["previousDirectory"] = settings["saveDirectory"]
  settings["saveDirectory"] = path
  with open("settings.json", "w") as jsonFile:
    jsonFile.write(json.dumps(settings, sort_keys=True, indent=4))

def usePrevDirectory():
  settings["saveDirectory"] = settings["previousDirectory"]
  with open("settings.json", "w") as jsonFile:
    jsonFile.write(json.dumps(settings, sort_keys=True, indent=4))

def downloadSongByQuery():
  query = sys.argv[1]

  verifyNoDuplicateSong(query)

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=query,
    part="id,snippet",
    maxResults=10
  ).execute()

  verifySearchResults(search_response)

  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      print "Attempting to download video: https://www.youtube.com/watch?v=" + search_result["id"]["videoId"]
      os.system("youtube-dl --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=" + search_result["id"]["videoId"])
      print "Renaming file to: " + query + ".mp3"
      print "File was saved in: " + settings["saveDirectory"]
      os.rename(search_result["snippet"]["title"] + "-" + search_result["id"]["videoId"] + ".mp3", query + ".mp3")
      sys.exit(0)

  print "No song with the specified duration +/- 5 seconds was found, are you sure you entered it correctly?"

def downloadSongByQueryAndDuration():
  query = sys.argv[1]
  givenDuration = map(int, sys.argv[2].split(":"))
  givenDuration = givenDuration[0] * 60 + givenDuration[1]

  verifyNoDuplicateSong(query)

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=query,
    part="id,snippet",
    maxResults=10
  ).execute()

  verifySearchResults(search_response)

  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      searchUrl = "https://www.googleapis.com/youtube/v3/videos?id="+search_result["id"]["videoId"]+"&key="+DEVELOPER_KEY+"&part=contentDetails"
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
        print "File was saved in: " + settings["saveDirectory"]
        os.rename(search_result["snippet"]["title"] + "-" + search_result["id"]["videoId"] + ".mp3", query + ".mp3")
        sys.exit(0)

  print "No song with the specified duration +/- 5 seconds was found, are you sure you entered it correctly?"

# Program Logic
arguments = iter(sys.argv)
for arg in arguments:
  if arg == "--help":
    printUsage()
    sys.exit(0)
  if arg == "--editSaveDirectory":
    path = arguments.next()
    editDownloadLocation(path)
    print "The download location was changed to: " + path
    sys.exit(0)
  if arg == "--usePrevDirectory":
    usePrevDirectory()
    print "The download location was changed to: " + settings["previousDirectory"]
    sys.exit(0)

if len(arguments) == 2:
  downloadSongByQuery()
elif len(arguments) == 3:
  downloadSongByQueryAndDuration()
else:
  print "There were " + str(len(arguments)) + " arguments given when 2 or 3 were expected"
  printUsage()
  sys.exit(-1)