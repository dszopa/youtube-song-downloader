from apiclient.discovery import build
import json
import urllib
import unicodedata
import sys
import os

query = sys.argv[1]
givenDuration = map(int, sys.argv[2].split(":"))
givenDuration = givenDuration[0] * 60 + givenDuration[1]

# Create directory variable
with open('downloadOptions.json') as data_file:    
    downloadOptions = json.load(data_file)

DEVELOPER_KEY = "AIzaSyAwF1yzv2ZA2kvKCOs0sRkYeXs5NnKDIFA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  developerKey=DEVELOPER_KEY)

search_response = youtube.search().list(
  q=query,
  part="id,snippet",
  maxResults=10
).execute()

if len(search_response.get("items", [])) == 0:
  print "There were no results for the specified song, are you sure you spelled it correctyl?"
  sys.exit(0)

for search_result in search_response.get("items", []):
  if search_result["id"]["kind"] == "youtube#video":
    searchUrl = "https://www.googleapis.com/youtube/v3/videos?id="+search_result["id"]["videoId"]+"&key="+DEVELOPER_KEY+"&part=contentDetails"
    response = urllib.urlopen(searchUrl).read()
    data = json.loads(response)
    all_data = data['items']
    contentDetails = all_data[0]['contentDetails']
    duration = map(int, str(contentDetails['duration'])[2:][:-1].split("M"))
    print duration

    if len(duration) > 1:
      duration = duration[0] * 60 + duration[1]
    else:
      if givenDuration < 60:
          duration = duration[1]
      else:
         duration = duration[0] * 60

    print duration - givenDuration
    if duration - givenDuration < 5 and duration - givenDuration > -5:
      os.chdir(downloadOptions["saveDirectory"])
      os.system("youtube-dl --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=" + search_result["id"]["videoId"])
      print "Renaming file to: " + query + ".mp3"
      print "File was saved in: " + downloadOptions["saveDirectory"]
      os.rename(search_result["snippet"]["title"] + "-" + search_result["id"]["videoId"] + ".mp3", query + ".mp3")
      sys.exit(0)

print "No song with the specified duration +/- 5 seconds was found, are you sure you entered it correctly?"