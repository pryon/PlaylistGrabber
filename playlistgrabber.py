#!/usr/bin/python3

"""YouTube Playlist Backup Script in Python3.

Save a YouTube playlist's video titles into a textfile.
"""

from apiclient.discovery import build
import argparse
import codecs
from datetime import datetime
from math import ceil
from os import linesep
from sys import getfilesystemencoding

RESULTS_PER_REQUEST = 50 # can only be between 1 and 50
OS_ENCODING = getfilesystemencoding()

class PlaylistGrabber:
    nextPageToken = ""
    
    def __init__(self, apiKey, playlistId, youtubeObj):
        self.apiKey = apiKey
        self.playlistId = playlistId
        self.youtubeObj = youtubeObj

    def forge_request(self):
        """Forge a request to the YouTube API and return it. When the request
        is executed, the response will be the requested data in JSON format.
        """
        playlistItemsListRequest = self.youtubeObj.playlistItems().list(
            playlistId=self.playlistId,
            part="snippet",
            maxResults=RESULTS_PER_REQUEST,
            key=self.apiKey,
            pageToken=self.nextPageToken
        )
        return playlistItemsListRequest

    def remove_disallowed_filename_chars(self, filename):
        """Remove characters that can't be inside filenames on most systems.
        Used this as a basis: https://stackoverflow.com/a/15908244
        """
        final = ""
        for char in filename:
            if char not in "<>:\"/\|?*" and ord(char) > 31:
                final += char
        if final.replace(".", "") == "":
            raise SystemError("The playlist\'s name is all periods")
        return final

    def get_date_str(self):
        """Return the current date in a concise string form."""
        now = datetime.now()
        return str(now.year) + ("{:02d}{:02d}".format(now.month, now.day))

    def get_clean_playlist_name(self):
        """Send a request for the playlist's title specifically and sanitize it."""
        playlistNameRequest = self.youtubeObj.playlists().list(
            id=self.playlistId,
            part="snippet",
            key=self.apiKey
        )
        playlistNameResponse = playlistNameRequest.execute()
        playlistName = playlistNameResponse["items"][0]["snippet"]["title"]
        return self.remove_disallowed_filename_chars(playlistName)

    def iterate_playlist(self, playlistItemsListResponse):
        """Forge a request as many times as necessary to append each element
        of the playlist to a list. Return the completed list.
        """
        totalResults = playlistItemsListResponse["pageInfo"]["totalResults"]
        requestsLeft = ceil(totalResults / RESULTS_PER_REQUEST)
        itemCounter = 0
        playlistItems = []

        while True:
            for item in playlistItemsListResponse["items"]:
                itemCounter += 1
                videoTitle = item["snippet"]["title"]
                currentLine = str(itemCounter) + ". " + videoTitle
                playlistItems.append(currentLine)
                # Using OS-specific encoding to avoid encoding exceptions 
                # when printing to console
                currentLine = (currentLine.encode(OS_ENCODING, errors="replace")) \
                    .decode(OS_ENCODING)
                print(currentLine)
            # last page, we're done
            if requestsLeft == 1:
                break
            else:
                self.nextPageToken = playlistItemsListResponse["nextPageToken"]
                requestsLeft -= 1
                playlistItemsListResponse = self.forge_request().execute()
        return playlistItems
      
    def list_to_file(self, playlistItems):
        """Write the list containing the playlist's items to a textfile."""
        filename = self.get_clean_playlist_name() + "_" + self.get_date_str() + ".txt"
        f = codecs.open(filename, mode="w", encoding="utf-8")
        for item in playlistItems:
            f.write(item + linesep)
        f.close()
    
    def run(self):
        initialResponse = self.forge_request().execute()
        self.list_to_file(self.iterate_playlist(initialResponse))

def cmdline_parse():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
            description="Save a YouTube playlist's contents into a textfile.")
    parser.add_argument("key",
                        help="Your Google Developer API key")
    parser.add_argument("id",
                        help="The ID of the YouTube playlist")
    return parser.parse_args()

def main():
    args = cmdline_parse()
    youtubeObj = build("youtube", "v3", developerKey=args.key) 
    grabber = PlaylistGrabber(args.key, args.id, youtubeObj)
    grabber.run()

if __name__ == "__main__":
    main()
