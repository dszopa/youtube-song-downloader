#!/usr/bin/env python

from apiclient.discovery import build
import json
import urllib
import os
import sys


class songDownloader(object):
    """Program Usage:
          Switches:
            --help
                Display the help screen.
            --changeSaveDir <Path>
                Change the download directory to <Path>
            --usePrevDir
                Revert the download directory to the previous directory.
            --link <Youtube URL>
                Download a song from the specified Youtube URL
            --exact
                Looks for a song with the exact duration specified.
            --buffer <BUFFER>
                Sets the buffer that duration can be to <BUFFER> seconds.
          Commands:
            python youtube-song-downloader.py Artist Name - Song Name Minutes:Seconds
                Download Song By Query and Duration. (Default 5 second buffer on duration)
            python youtube-song-downloader.py Artist Name - Song Name
                Download Song by Query.
    """

    def __init__(self):
        self.DEVELOPER_KEY = "AIzaSyAwF1yzv2ZA2kvKCOs0sRkYeXs5NnKDIFA"
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"

        with open('settings.json', 'r') as data_file:
            self.settings = json.load(data_file)

        if not os.path.exists(self.settings["saveDirectory"]):
            print "The specified save directory " + self.settings["saveDirectory"] + " does not exist!"
            print "Please use --changeSaveDir <Path> to set the save directory"
            sys.exit(-1)

    def printUsage(self):
        print "Program Usage:"
        print "  Switches:"
        print "\t--help"
        print "\t\tDisplay the help screen"
        print "\t--changeSaveDir <Path>"
        print "\t\tChange the download directory to <Path>"
        print "\t--usePrevDir"
        print "\t\tRevert the download directory to the previous directory"
        print "  Commands:"
        print "\tpython downloadSong.py \"Artist Name - Song Name\" \"Minutes:Seconds\""
        print "\t\tDownload Song By Query and Duration."
        print "\tpython downloadSong.py \"Artist Name - Song Name\""
        print "\t\tDownload Song by Query."

    def verifyNoDuplicateSong(self, query):
        filesInDirectory = os.listdir(os.getcwd())
        for fileName in filesInDirectory:
            if fileName == query + ".mp3":
                print "The desired song \"" + query + ".mp3\" already exists in the directory"
                return False
        return True

    def verifySearchResults(self, search_response):
        if len(search_response.get("items", [])) == 0:
            print "There were no results for the specified song, are you sure you entered it correctly?"
            return False
        else:
            return True

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

    def downloadSongByQuery(self, query):
        os.chdir(self.settings["saveDirectory"])

        if self.verifyNoDuplicateSong(query) != True:
            return None

        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                        developerKey=self.DEVELOPER_KEY)

        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=10
        ).execute()

        if self.verifySearchResults(search_response) != True:
            return None

        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                print "Attempting to download video: https://www.youtube.com/watch?v=" + search_result["id"]["videoId"]
                os.system("youtube-dl --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=" + search_result["id"]["videoId"])
                print "Renaming file to: " + query + ".mp3"

                temp = search_result["snippet"]["title"].replace("\"", "\'").replace("|", "_")
                if os.path.exists(temp + "-" + search_result["id"]["videoId"] + ".mp3"):
                    os.rename(temp + "-" + search_result["id"]["videoId"] + ".mp3", query + ".mp3")
                    print "File was saved in: " + self.settings["saveDirectory"]
                    return None
                else:
                    print "Unable to rename file: " + temp + "-" + search_result["id"]["videoId"] + ".mp3" + "was not found"
                    return None

        print "No song with the specified duration +/- 5 seconds was found, are you sure you entered it correctly?"

    def downloadSongByQueryAndDuration(self, query, duration, buf):
        givenDuration = map(int, duration.split(":"))
        givenDuration = givenDuration[0] * 60 + givenDuration[1]

        os.chdir(self.settings["saveDirectory"])

        if self.verifyNoDuplicateSong(query) is not True:
            return None

        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                        developerKey=self.DEVELOPER_KEY)

        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=10
        ).execute()

        if self.verifySearchResults(search_response) is not True:
            return None

        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                searchUrl = "https://www.googleapis.com/youtube/v3/videos?id=" + \
                            search_result["id"]["videoId"]+"&key=" + \
                            self.DEVELOPER_KEY+"&part=contentDetails"
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

                if duration - givenDuration <= buf and duration - givenDuration >= buf * -1:
                    print "Attempting to download video: https://www.youtube.com/watch?v=" + search_result["id"]["videoId"]
                    os.system("youtube-dl --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=" + search_result["id"]["videoId"])
                    print "Renaming file to: " + query + ".mp3"

                    temp = search_result["snippet"]["title"].replace("\"", "\'").replace("|", "_")
                    if os.path.exists(temp + "-" + search_result["id"]["videoId"] + ".mp3"):
                        os.rename(temp + "-" + search_result["id"]["videoId"] + ".mp3", query + ".mp3")
                        print "File was saved in: " + self.settings["saveDirectory"]
                        print "The file downloaded had a difference of " + str(duration - givenDuration) + " seconds from the specified duration"
                        return None
                    else:
                        print "Unable to rename file: " + temp + "-" + search_result["id"]["videoId"] + ".mp3" + "was not found"
                        return None

        print "No song with the specified duration +/- " + str(buf) + " seconds was found, are you sure you entered it correctly?"

    def downloadSongByYoutubeLink(self, link):
        print "Attempting to download video: " + link
        os.chdir(self.settings["saveDirectory"])
        os.system("youtube-dl --extract-audio --audio-format mp3 " + link)
