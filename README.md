YouTube Playlist Backup Script in Python3
=========================================


This script can be used to save a YouTube playlist's video titles into a textfile.

The script should be able to handle all kinds of Unicode text, whether it's in the playlist's name or in the video title itself. The created textfile uses UTF-8 encoding by default.


Purpose
-------------

This can be a useful tool if you own a playlist that has videos which
are likely to be removed/made private in the future, and you want to
keep track of them, e.g. unreleased songs on unofficial music promotion
channels.

As it's not using authentication, you can only run the script on public
and unlisted playlists.


Usage
-------------

To use it yourself, you're going to need a Google account,
a Google Developers Console Project with an API key for the YouTube API,
and of course, a playlist.

You can get the playlist's ID from the playlist's URL, e.g. in:
```https://www.youtube.com/playlist?list=PLf938G28Gx```
where the playlist's ID is:
```PLf938G28Gx```

Info on setting up a Google Dev Project and getting an API key:
https://developers.google.com/g_youtube/v3/getting-started

The Google Dev API for Python can be installed using pip:
```$ pip install --upgrade google-api-python-client```