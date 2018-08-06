Riker
=====

Companion program to [MusicBrainz Picard](https://picard.musicbrainz.org/) where
Picard properly tags music files and then Riker moves them to the appropriate place
on the filesystem, mimicing how iTunes 'Automatically Add to iTunes' feature works.

Running Riker causes it to watch a folder or any new MP3 file creation events (such as
moving a file into the directory). When that happens, it gets the file's ID3 tags and
then moves the file based on that. The constructed path is:
`/artist/album/track title.mp3`
where `artist`, `album`, and `title` are all truncated to a max of 40 characters and 
`track` is left-padded by the max number of tracks (so if the album has 16 tracks
and it's looking at track 2, then `track` will be `02`).

Requirements
------------
* watchdog
* eyeD3
* python-magic

Usage
-----
```
riker.py
```

Settings
-----------
At the top of Riker, there are two global variables `WATCH_FOLDER` and `MUSIC_FOLDER`.
Set these to point to the folder on your filesystem that you want to watch 
(`WATCH_FOLDER`) and move files into (`MUSIC_FOLDER`).
