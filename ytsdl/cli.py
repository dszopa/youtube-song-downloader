#!/usr/bin/env python

import sys
import os
import songDownloader


def main():
    # Need this line to import settings.json
    os.chdir(os.path.dirname(songDownloader.__file__))
    arguments = iter(sys.argv)
    sd = songDownloader.songDownloader()
    buf = 5  # buffer is default of 5
    queryIndex = 1
    argCount = len(sys.argv)
    for index, arg in enumerate(arguments):
        if arg == "--help" or arg == "-h":
            sd.printUsage()
            sys.exit(0)
        if arg == "--changeSaveDir":
            path = arguments.next()
            sd.editDownloadLocation(path)
            print "The download location was changed to: " + path
            sys.exit(0)
        if arg == "--usePrevDir":
            sd.usePrevDirectory()
            sys.exit(0)
        if arg == "--link":
            sd.downloadSongByYoutubeLink(arguments.next())
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
        sd.downloadSongByQuery(sys.argv[queryIndex])
    elif argCount == 3:
        sd.downloadSongByQueryAndDuration(sys.argv[queryIndex], sys.argv[queryIndex+1], buf)
    else:
        print "Invalid number of arguments given"
        sd.printUsage()
        sys.exit(-1)

if __name__ == "__main__":
    main()
