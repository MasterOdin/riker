#!/usr/bin/env python3

from argparse import ArgumentParser
import os
from pathlib import Path
import time

from eyed3.mp3 import Mp3AudioFile
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

VERSION = "0.1.0"

WATCH_FOLDER = Path("E:/", "picard", "watch")
MUSIC_FOLDER = Path("E:/", "picard", "music")


def cleanup(file_path):
    """
    Given a folder, iterate up the tree cleaning out directories until we hit a
    mp3 file on the way up
    """
    while True:
        if file_path == WATCH_FOLDER:
            return
        print(str(file_path) + " -> ", end="")
        for entry in file_path.iterdir():
            if entry.is_file():
                if entry.suffix != ".mp3":
                    entry.unlink()
                else:
                    print(str(entry.name))
                    return
        for entry in file_path.iterdir():
            if len(os.listdir()) == 0:
                entry.rmdir()
        file_path.rmdir()
        file_path = file_path.parent


def clean_text(string):
    """
    Cleans a string of any characters that are invalid for the given filesystem, replacing them
    with the underscore ('_') character instead.

    < (less than)
    > (greater than)
    : (colon - sometimes works, but is actually NTFS Alternate Data Streams)
    " (double quote)
    / (forward slash)
    \ (backslash)
    | (vertical bar or pipe)
    ? (question mark)
    * (asterisk)
    """
    for char in ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]:
        string = string.replace(char, "_")
    return string


class MusicHandler(PatternMatchingEventHandler):
    patterns = ["*.mp3"]

    def on_modified(self, event):
        src = Path(event.src_path).resolve()
        historical_size = -1
        while historical_size != src.stat().st_size:
            historical_size = src.stat().st_size
            time.sleep(1)

        print("-> new file {}".format(src.name))
        mp3_file = Mp3AudioFile(str(src))
        artist = clean_text(mp3_file.tag.album_artist[:40])
        album = clean_text(mp3_file.tag.album[:40])
        track = str(mp3_file.tag.track_num[0]).zfill(
            len(str(mp3_file.tag.track_num[1]))
        )
        if mp3_file.tag.disc_num[1] != 1:
            disc_num = str(mp3_file.tag.disc_num[0]).zfill(
                len(str(mp3_file.tag.disc_num[1]))
            )
            track = f"{disc_num}-{track}"
        title = clean_text(mp3_file.tag.title[:40])
        filename = "{} {}.mp3".format(track, title)
        dest = Path(MUSIC_FOLDER, artist, album, filename)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            dest.unlink()
        src.rename(dest)
        cleanup(src.parent)


def args():
    parser = ArgumentParser(description="Riker - companion to MusicBrainz's Picard")
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s {}".format(VERSION)
    )
    parser.add_argument("--config", type=str, default="riker.json")
    return parser.parse_args()


def main():
    if not WATCH_FOLDER.exists() or not MUSIC_FOLDER.exists():
        raise SystemExit("WATCH_FOLDER or MUSIC_FOLDER do not exist")

    print("Watching {}...".format(str(WATCH_FOLDER)))
    observer = Observer()
    observer.schedule(MusicHandler(), str(WATCH_FOLDER))
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
