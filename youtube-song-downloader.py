#!/usr/bin/env python

import ytsdl
import sys
import os

# Program Logic
arguments = iter(sys.argv)
songDownloader = ytsdl.songDownloader()
buf = 5 # buffer is default of 5
queryStart = 1
argCount = len(sys.argv)
for index, arg in enumerate(arguments):
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
  if arg == "--exact":
    print index
    if index <= queryStart:
      queryStart += 1
    buf = 0
    argCount -= 1
  if arg == "--buffer":
    if index <= queryStart:
      queryStart += 2
    buf = int(arguments.next())
    argCount -= 2

# TODO because you can specify switches the location of query and duration can change, how to account for this?
if argCount == 2:
  songDownloader.downloadSongByQuery(sys.argv[queryStart])
elif argCount == 3:
  songDownloader.downloadSongByQueryAndDuration(sys.argv[queryStart], sys.argv[queryStart+1], buf)
else:
  print "Invalid number of arguments given"
  songDownloader.printUsage()
  sys.exit(-1)