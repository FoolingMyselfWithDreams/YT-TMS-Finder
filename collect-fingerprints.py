#!/usr/bin/python3
import os
import libs.fingerprint as fingerprint

from termcolor import colored
from libs.reader_file import FileReader
from libs.db_sqlite import SqliteDatabase
from libs.config import get_config
from pydub import AudioSegment

if __name__ == "__main__":
    config = get_config()

    db = SqliteDatabase()
    path = "samples/"

    # fingerprint all files in a directory

    for filename in os.listdir(path):
        songname, extension = os.path.splitext(os.path.basename(filename))
        if extension.lower() in [".flac", ".wav", ".mp3"]: #.ogg
            # convert all audio files to mp3 and 44kHz to normalize the fingerprints
            song = AudioSegment.from_file(path + filename)
            if extension.lower() == ".mp3" and song.frame_rate == 44100:
                reader = FileReader(path + filename)
                pass
            else:
                song.export("tmp.mp3", format="mp3", parameters=["-ar", "44100", "-b:a", "320k"])
                reader = FileReader("tmp.mp3")

                                 
            audio = reader.parse_audio()

            song = db.get_song_by_filehash(audio["file_hash"])
            song_id = db.add_song(filename, audio["file_hash"])

            msg = " * %s %s: %s" % (
                colored("id=%s", "white", attrs=["dark"]),  # id
                colored("channels=%d", "white", attrs=["dark"]),  # channels
                colored("%s", "white", attrs=["bold"]),  # filename
            )
            print(msg % (song_id, len(audio["channels"]), filename))

            if song:
                hash_count = db.get_song_hashes_count(song_id)

                if hash_count > 0:
                    msg = "   already exists (%d hashes), skip" % hash_count
                    print(colored(msg, "red"))

                    continue

            print(colored("   new song, going to analyze..", "green"))

            hashes = set()
            channel_amount = len(audio["channels"])

            for channeln, channel in enumerate(audio["channels"]):
                msg = "   fingerprinting channel %d/%d"
                print(
                    colored(msg, attrs=["dark"])
                    % (channeln + 1, channel_amount)
                )

                channel_hashes = fingerprint.fingerprint(
                    channel,
                    Fs=audio["Fs"],
                    plots=config["fingerprint.show_plots"],
                )
                channel_hashes = set(channel_hashes)

                msg = "   finished channel %d/%d, got %d hashes"
                print(
                    colored(msg, attrs=["dark"])
                    % (channeln + 1, channel_amount, len(channel_hashes))
                )

                hashes |= channel_hashes

            msg = "   finished fingerprinting, got %d unique hashes"

            values = []
            for hash, offset in hashes:
                values.append((song_id, hash, offset))

            msg = "   storing %d hashes in db" % len(values)
            print(colored(msg, "green"))

            db.store_fingerprints(values)

            try:
                os.remove("tmp.mp3")
            except FileNotFoundError:
                pass

    print("done with fingerprinting files")
