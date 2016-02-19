#!/usr/bin/env python

from ytsdl.songDownloader import songDownloader
import sys
import os

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
  if arg == "--link":
    songDownloader.downloadSongByYoutubeLink(arguments.next())
    sys.exit(0)

if len(sys.argv) == 2:
  songDownloader.downloadSongByQuery(sys.argv[1])
elif len(sys.argv) == 3:
  songDownloader.downloadSongByQueryAndDuration(sys.argv[1], sys.argv[2])
else:
  print "There were " + str(len(sys.argv)) + " arguments given when 2 or 3 were expected"
  songDownloader.printUsage()
  sys.exit(-1)