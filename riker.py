#!/usr/bin/env python3

from pathlib import Path
import time

from eyed3.mp3 import Mp3AudioFile
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


WATCH_FOLDER = Path('E:/', 'picard', 'watch')
MUSIC_FOLDER = Path('E:/', 'My Music')

class MusicHandler(PatternMatchingEventHandler):
    patterns = ['*.mp3']

    def on_created(self, event):
        src = Path(event.src_path).resolve()
        mp3_file = Mp3AudioFile(str(src))
        artist = mp3_file.tag.artist[:40]
        album = mp3_file.tag.album[:40]
        track = str(mp3_file.tag.track_num[0]).zfill(len(str(mp3_file.tag.track_num[1])))
        title = mp3_file.tag.title[:40]
        filename = "{} {}.mp3".format(track, title)      
        dest = Path(MUSIC_FOLDER, artist, album, filename)
        dest.parent.mkdir(parents=True, exist_ok=True)
        print("handling {}. moving to {}.".format(src, dest))
        src.rename(dest)

def main():
    if not WATCH_FOLDER.exists() or not MUSIC_FOLDER.exists():
        raise SystemExit('WATCH_FOLDER or MUSIC_FOLDER do not exist')
    
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

if __name__ == '__main__':
    main()