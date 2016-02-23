#!/usr/bin/env python

import sys
import os
import ytsdl

def main():
  os.chdir(os.path.dirname(ytsdl.__file__))
  arguments = iter(sys.argv)
  songDownloader = ytsdl.songDownloader()
  buf = 5 # buffer is default of 5
  queryIndex = 1
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
      if index <= queryIndex:
        queryIndex += 1
      buf = 0
      argCount -= 1
    if arg == "--buffer":
      if index <= queryIndex:
        queryIndex += 2
      buf = int(arguments.next())
      argCount -= 2

  if argCount == 2:
    songDownloader.downloadSongByQuery(sys.argv[queryIndex])
  elif argCount == 3:
    songDownloader.downloadSongByQueryAndDuration(sys.argv[queryIndex], sys.argv[queryIndex+1], buf)
  else:
    print "Invalid number of arguments given"
    songDownloader.printUsage()
    sys.exit(-1)

if __name__ == "__main__":
  main()
