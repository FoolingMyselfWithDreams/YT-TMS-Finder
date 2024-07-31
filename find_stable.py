import argparse                             #for getting command line arguments
import os                                   #for various things
from selenium import webdriver, common      #for getting html source of channel
from time import sleep                      #to prevent errors
import re                       
import bs4 as bs                            #for working with html source file
import subprocess                           #calling other script or executables from this file
import sys
from termcolor import *                     #for getting colored text

from libs.db_sqlite import SqliteDatabase   #for working with the SQL database
from recognize_from_file import run_recognition
from libs.utils import align_matches
from pydub import AudioSegment
import math
import datetime                             # To include time info in the missed.txt file                              
from datetime import datetime, time, date   
import time as tm                           # for getting script runtime

import yt_dlp
import threading
from ExcThread import ExcThread
#import multiprocessing

### vars for script runtime and missed.txt time
now = datetime.now()

currentTime = time(now.hour, now.minute, now.second)
currentDate = date(now.year, now.month, now.day)
start_time = tm.time()

#sys.tracebacklimit = 0


print(r"""
Welcome to...

__   _______   ________  ___ _____  ______ _           _           
\ \ / /_   _| |_   _|  \/  |/  ___| |  ___(_)         | |          
 \ V /  | |     | | | .  . |\ `--.  | |_   _ _ __   __| | ___ _ __ 
  \ /   | |     | | | |\/| | `--. \ |  _| | | '_ \ / _` |/ _ \ '__|
  | |   | |     | | | |  | |/\__/ / | |   | | | | | (_| |  __/ |   
  \_/   \_/     \_/ \_|  |_/\____/  \_|   |_|_| |_|\__,_|\___|_|   
                                                                   
                                                                      
""")


class Finder:
    def __init__(self):        
        ### Verifying needed folders
        if not os.path.isdir("downloaded_mp3s"):
            os.mkdir("downloaded_mp3s")
        
        ### setting variables
        self.arguments = get_arguments()
        self.sql = SqliteDatabase()
        
        assert 4 - [self.arguments.id, self.arguments.restore_file, self.arguments.channel_url, self.arguments.url_file].count(None) <= 1 , "Can't have any of the ID, channel, URL file or restore file as combined arguments."
        
        # if there is no url or id, ask for url
        if (self.arguments.id is None and self.arguments.channel_url is None and self.arguments.restore_file is None and self.arguments.url_file is None):
            expr_yesno = r"^[YN]$"
            yesnoQuery = input("Check multiple channels and playlists through a filled urls.txt file? Y/N ")
            while re.match(expr_yesno, yesnoQuery, re.I) is None:
                print("Invalid input")
                yesnoQuery = input()
            if yesnoQuery.upper() == "Y":
                try:
                    if os.path.getsize("urls.txt") > 0:
                        self.arguments.url_file = True
                        self.url_file = True
                    else: raise Exception
                except: 
                    cprint("Error: urls.txt was not found or had no contents. Please create it in this program's folder or add URLs to it (one on each line) and restart this program.", "red")
                    exit()
            elif yesnoQuery.upper() == "N":
                self.arguments.url_file = None
                self.url_file = None
                print(r"""Enter a channel URL or playlist URL to begin.
         Example URL:  https://www.youtube.com/@texticks/videos""")
                self.arguments.channel_url = input("URL: ")   #Example input: www.youtube.com/@GlitchxCity/videos
        
        # if there is a url, verify if it's a correct URL
        if self.arguments.channel_url is not None:
            self.verify_url(self.arguments.channel_url)

        # if no arguments were given by the user, ask for verbose, min-duration, max-duration and threads
        if len(sys.argv) == 1:
            expr_yesno = r"^[YN]$"
            yesnoQuery = input("Do you want to use advanced search options? Y/N ")
            while re.match(expr_yesno, yesnoQuery, re.I) is None:
                print("Invalid input")
                yesnoQuery = input()
            if yesnoQuery.upper() == "Y":
                yesnoQuery = input("Display detailed messaging and completion percentage? Y/N ")
                while re.match(expr_yesno, yesnoQuery, re.I) is None:
                    print("Invalid input")
                    yesnoQuery = input()
                if yesnoQuery.upper() == "Y":
                    self.arguments.verbose = True
                elif yesnoQuery.upper() == "N":
                    pass

                yesnoQuery = input("Ignore already checked videos? Y/N ")
                while re.match(expr_yesno, yesnoQuery, re.I) is None:
                    print("Invalid input")
                    yesnoQuery = input()
                if yesnoQuery.upper() == "Y":
                    self.arguments.ignore = True
                elif yesnoQuery.upper() == "N":
                    pass

                expr_duration = r"^(?:\d{1,2}:)?(?=[0-5]?\d:)([0-5]?\d:)?(?:[0-5]?\d)$"
                minQuery = input("Set minimum duration of video length (min 0:00 (or no input), max 99:59:59): ")
                while re.match(expr_duration, minQuery) is None and minQuery != "":
                    print("Invalid input")
                    minQuery = input()
                if minQuery == "": pass
                else: self.arguments.min_duration = self.countseconds(minQuery)

                maxQuery = input("Set maximum duration of video length (min 0:00, max 99:59:59 (or no input)): ")
                while re.match(expr_duration, maxQuery) is None and maxQuery != "":
                    print("Invalid input")
                    maxQuery = input()
                if maxQuery == "": pass
                else: self.arguments.max_duration = self.countseconds(maxQuery)

                titleQuery = input("Use \"text\" to set anything that must be part of the title, use !\"text\" to set anything that can't be part of the title, no commas as seperator needed. Add one + without quotes if at least one \"text\" has to match rather than all of them (or no input to skip): ")
                while self.verify_titles(titleQuery) is None and titleQuery != "":
                    print("Invalid input")
                    titleQuery = input()
                if titleQuery == "": pass
                else:
                    self.arguments.title = titleQuery
                    print("Title sets are: " + " ".join(self.arguments.title.split()))

                threadQuestion = "How many videos should be downloaded and checked at the same time? (recommended: 1 to 3): "
                threadQuery = input(threadQuestion)
                while threadQuery != "":
                    if re.match(r"^[1-9]\d*$", threadQuery) is None:
                        print("Invalid input")
                        threadQuery = input()
                    else:
                        if int(threadQuery) > 3 :
                            cprint("\nWARNING: Temporary IP bans might occur while using a high number of frequent downloads.", "red")
                            cprint("Do you want to proceed with " + threadQuery + " simultaneous downloads? Y/N ")
                            yesnoQuery = input()
                            while re.match(expr_yesno, yesnoQuery, re.I) is None:
                                print("Invalid input")
                                yesnoQuery = input()
                            if yesnoQuery.upper() == "Y":
                                break
                            else:
                                threadQuery = input(threadQuestion)
                        elif int(threadQuery) <= 3:
                            break
                if threadQuery == "": threadQuery = None
                else: self.arguments.threads = int(threadQuery)
                
            elif yesnoQuery.upper() == "N":
                yesnoQuery = input("Display detailed messaging and completion percentage? Y/N ")
                while re.match(expr_yesno, yesnoQuery, re.I) is None:
                    print("Invalid input")
                    yesnoQuery = input()
                if yesnoQuery.upper() == "Y":
                    self.arguments.verbose = True
                elif yesnoQuery.upper() == "N":
                    pass

                yesnoQuery = input("Ignore already checked videos? Y/N ")
                while re.match(expr_yesno, yesnoQuery, re.I) is None:
                    print("Invalid input")
                    yesnoQuery = input()
                if yesnoQuery.upper() == "Y":
                    self.arguments.ignore = True
                elif yesnoQuery.upper() == "N":
                    pass

                threadQuestion = "How many videos should be downloaded and checked at the same time? (recommended: 1 to 3): "
                threadQuery = input(threadQuestion)
                while threadQuery != "":
                    if re.match(r"^[1-9]\d*$", threadQuery) is None:
                        print("Invalid input")
                        threadQuery = input()
                    else:
                        if int(threadQuery) > 3 :
                            cprint("\nWARNING: Temporary IP bans might occur while using a high number of frequent downloads.", "red")
                            cprint("Do you want to proceed with " + threadQuery + " simultaneous downloads? Y/N ")
                            yesnoQuery = input()
                            while re.match(expr_yesno, yesnoQuery, re.I) is None:
                                print("Invalid input")
                                yesnoQuery = input()
                            if yesnoQuery.upper() == "Y":
                                break
                            else:
                                threadQuery = input(threadQuestion)
                        elif int(threadQuery) <= 3:
                            break
                if threadQuery == "": threadQuery = None
                else: self.arguments.threads = int(threadQuery)
        
        self.ignore_checked = self.arguments.ignore
        self.verbose = self.arguments.verbose
        self.speedmode = self.arguments.speedmode
        self.title = self.arguments.title
        self.url_file = self.arguments.url_file
        self.html_urls = self.arguments.html_urls
        self.vprint(str(self.arguments), "yellow")
        
        ### Make sure that there are no leftovers from previous runs
        self.delete_mp3s()

    def countseconds(self, len):
        seconds = 0
        for x in len.split(':'):
            seconds = seconds * 60 + int(x)
        return seconds
    
    def verify_titles(self, titles):
        titles = titles.split()
        for idx, x in enumerate(titles, 1):
            if re.match(r"^\+$|^\".*\"|^!\".*\"", x):
                if(idx == len(titles)):
                    return True
            else:
                return None
        
        
    def verify_url(self, url):
        ### Check if the channel url is in right format
        expr_channel = r"^.*(/c(hannel)?/[a-zA-Z0-9-_]+)"
        expr_user    = r"^.*(/u(ser)?/[a-zA-Z0-9-_]+)"
        expr_at      = r"^.*(/@[a-zA-Z0-9-_]+)"
        expr_playlist = r"^.*(/playlist\?list=[a-zA-Z0-9-_]+)"

        channel_path_match = None
        user_path_match = None
        at_path_match = None
        playlist_path_match = None

        while channel_path_match is None and user_path_match is None and at_path_match is None and playlist_path_match is None:
            channel_path_match = re.match(expr_channel, url)
            user_path_match = re.match(expr_user, url)
            at_path_match = re.match(expr_at, url)
            playlist_path_match = re.match(expr_playlist, url)
            if channel_path_match is not None:
                channel_path = channel_path_match.groups()[0]
                self.channel_url = "https://www.youtube.com" + channel_path + "/videos"
                return True
            elif user_path_match is not None:
                channel_path = user_path_match.groups()[0]
                self.channel_url = "https://www.youtube.com" + channel_path + "/videos"
                return True
            elif at_path_match is not None:
                channel_path = at_path_match.groups()[0]
                self.channel_url = "https://www.youtube.com" + channel_path + "/videos"
                return True
            elif playlist_path_match is not None:
                channel_path = playlist_path_match.groups()[0]
                self.channel_url = "https://www.youtube.com" + channel_path
                return True
            
            if self.arguments.url_file is not None or self.url_file is not None:
                cprint("URL {url} in urls.txt is invalid. Please check missed.txt for any invalid channel or playlist URLs.", "red")
                with open("missed.txt", "a") as f:
                    f.write(f"{currentDate} {currentTime}: (Invalid URL) Could not check channel or playlist '{url}'.\n")
                return False
            else: url = input("The URL you entered is invalid. Please enter a valid URL: ")
    
    
    def vprint(self, text: str, colour:str = "white"):
        """
        Helpful function for printing when verbose is turned on
        """
        if self.verbose:
            cprint(text, colour)
    
    
    def get_song_mp3_do_not_use2(self, id:str) -> str:
        """
        Downloads the audio from a youtube video in mp3 format given a video id.
        """
        dir_here = os.path.abspath(os.getcwd())
        dir_mp3s = os.path.join(dir_here, "downloaded_mp3s")

        url = "https://youtube.com/watch?v=" + id
        interm_out = os.path.join(dir_mp3s, f"{id}.%(ext)s")


        postprocessor_args = []
        postprocessor_args.extend(["-ss", "00:00:00.00"])
        postprocessor_args.extend(["-t", "00:00:15.00"])

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": interm_out,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                }
            ],
            "postprocessor_args": postprocessor_args,
            "quiet": True,
            "no_warnings": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        self.vprint(f"Audio downloaded! Performing fingerprint match scan...")

        return os.path.abspath(os.path.join("downloaded_mp3s", os.listdir("downloaded_mp3s")[0]))


    def get_song_mp3(self, id: str) -> str:
        """
        Downloads the audio from a youtube video in mp3 format given a video id.
        """
        
        ### Delete existing mp3 files in downloaded_mp3s directory in case there is one left of a previous run
        #self.delete_mp3s()
        url = "https://youtube.com/watch?v=" + id
        
        dir_here = os.path.abspath(os.getcwd())
        dir_yt_dlp_dir = os.path.join(dir_here, "yt-dlp")
        
        ### Set yt-dlp exectuable for windows and linux users
        if sys.platform == "win32":
            yt_dlp_exec = "yt-dlp.exe"
        else:
            yt_dlp_exec = "yt-dlp"
        path_yt_dlp_exec = os.path.join(dir_yt_dlp_dir, yt_dlp_exec)
        
        ### initialise this variable to make the destination argument for the yt-dlp command
        dir_downloaded_mp3s = os.path.join(dir_here, "downloaded_mp3s")
    
        ### '%(title)s.%(ext)s' comes from how yt-dlp.exe outputs files with 
        ### filename as youtube title
        #destination_arg = os.path.join(dir_downloaded_mp3s, "%(title)s.%(ext)s")
        destination_arg = os.path.join(dir_downloaded_mp3s, f"{id}.%(ext)s")
        
        ### Make the mp3 folder which will contain a downloaded mp3
        if not os.path.isdir(dir_downloaded_mp3s):
            os.mkdir(dir_downloaded_mp3s)
        
        ### Setting up the command for the different modes
        if not self.speedmode:
            cmd = [
                    #"yt-dlp", "-x", "--audio-format", "mp3", "-f", "\"[asr>44000]\"", "--sleep-requests 1", "--sleep-interval 1", "--max-sleep-interval 2",
                    #"--no-warnings", f"{url}", "-o", f"{destination_arg}"
                    "yt-dlp", "-f", "\"m4a [asr>44000]\"", "--sleep-requests 1", "--sleep-interval 1", "--max-sleep-interval 2",
                    "--no-warnings", f"{url}", "-o", f"{destination_arg}"
                ]
        else:
            cmd = [
                    #"yt-dlp", "-x", "--audio-format", "mp3", "-f", "\"[asr>44000]\"", "--sleep-requests 1", "--sleep-interval 1", "--max-sleep-interval 2", 
                    #"--no-warnings", "--postprocessor-args", "\"-ss 00:00:00.00 -t 00:00:15.00\"", f"{url}", "-o", f"{destination_arg}"
                    "yt-dlp", "-f", "\"m4a [asr>44000]\"", "--sleep-requests 1", "--sleep-interval 1", "--max-sleep-interval 2", 
                    "--no-warnings", "--postprocessor-args", "\"-ss 00:00:00.00 -t 00:00:15.00\"", f"{url}", "-o", f"{destination_arg}"
                ]
        
        try:
            subprocess.check_output(' '.join(cmd))
            sleep(0.1)
            self.vprint(f"Audio downloaded! Performing fingerprint match scan...")
        except KeyboardInterrupt:
            ### completely exit program if this is what user wants
            self.delete_mp3s()
            exit()
        except:
            ### always show error even when verbose is off
            try:
                if not os.path.isfile(destination_arg):
                    print("Retrying to download in different format...")
                    if not self.speedmode:
                        cmd = [
                            "yt-dlp", "-f", "\"m4a, [asr>44000]\"", "--sleep-requests 1", "--sleep-interval 1", "--max-sleep-interval 2",
                            "--no-warnings", f"{url}", "-o", f"{destination_arg}"
                        ]
                    else:
                        cmd = [
                            "yt-dlp", "-f", "\"m4a, [asr>44000]\"", "--sleep-requests 1", "--sleep-interval 1", "--max-sleep-interval 2", 
                            "--no-warnings", "--postprocessor-args", "\"-ss 00:00:00.00 -t 00:00:15.00\"", f"{url}", "-o", f"{destination_arg}"
                        ]
                    subprocess.check_output(' '.join(cmd))
                    sleep(0.1)
                    tmpFilePath = os.path.join(dir_downloaded_mp3s, f"{id}" + ".m4a")
                    song = AudioSegment.from_file(tmpFilePath)
                    song.export(os.path.join(dir_downloaded_mp3s, f"{id}.mp3"), format="mp3", parameters=["-ar", "44100", "-b:a", "320k"])
                    try:
                        os.remove(tmpFilePath)
                    except OSError:
                        pass
                    self.vprint(f"Audio downloaded! Performing fingerprint match scan...")
                    return os.path.abspath(os.path.join("downloaded_mp3s", os.listdir("downloaded_mp3s")[0]))
            except KeyboardInterrupt:
                ### completely exit program if this is what user wants
                self.delete_mp3s()
                exit()
            cprint("Video audio couldn't be downloaded. Skipping for now. Please check missed.txt for more info.", "red")
            with open("missed.txt", "a") as f:
                f.write(f"{currentDate} {currentTime}: Could not check video with ID {id}. Please copy and paste this URL in your browser to check: 'youtube.com/watch?v={id}'\n")
            ### when return value is None, we go to the next song to check
            return None
        
        ### Even though this may not be the best way to do it, this does support greek letters on both Windows and Linux 
        return os.path.abspath(os.path.join("downloaded_mp3s", os.listdir("downloaded_mp3s")[0]))
        
    
    
    def delete_mp3s(self):
        """
        Deletes all mp3s in the mp3s folder.
        """
        current_directory = os.getcwd()
        for file in os.listdir("downloaded_mp3s"):
            full_path = os.path.join(current_directory, "downloaded_mp3s", file)
            try:
                os.remove(full_path)
            except OSError:
                pass
    
    
    def get_channel_source(self):
        ### if a restore file is supplied, use that instead
        if self.arguments.restore_file is not None:
            with open(self.arguments.restore_file) as f:
                source = f.read()
            return source
        
        ### Open a browser and catch chromedriver not found error
        try:
            driver = webdriver.Chrome()
        except common.exceptions.WebDriverException:
            try:
                driver = webdriver.Chrome(executable_path = r"C:\ProgramData\chocolatey\bin\chromedriver.exe")
            except:
                print("If you see this message, that means selenium can't find 'chromedriver.exe.'")
                print("To fix this, search for 'chromedriver.exe' on your file system.")
                print(r"Example of 'chromedriver.exe' path: 'C:\ProgramData\chocolatey\bin\chromedriver.exe'")
                location = input("Once you've found 'chromedriver.exe', paste the location to it here: ")
                driver = webdriver.Chrome(executable_path = location)
                print("Alternatively, you can put it in the code yourself so you don't have to constantly fill this in.")
                print("To do that, in the file 'find_stable.py', search for the line \"driver = webdriver.Chrome()\" and in between the brackets put:")
                print("executable_path = (your chromedriver location)")
        
        
        driver.get(self.channel_url)
        sleep(5)
        source = driver.page_source
        
        ### Keep scrolling until we hit the end of the page
        scroll_by = 5000
        driver.execute_script(f"window.scrollBy(0, {scroll_by});")
        while driver.page_source != source:
            source = driver.page_source
            driver.execute_script(f"window.scrollBy(0, {scroll_by});")
            sleep(0.1)
        driver.quit()
        
        with open("restore_file.html", "w") as f:
            f.write(source.encode('utf-8').decode('ascii','ignore'))
        
        return source
    
    
    def check_file(self, fpath, thresh=20):
        """
        Fingerprint and try to match a song against database
        """
        ### Getting ID from filepath, Might just supply ID as argument
        base = os.path.basename(fpath)
        id_, _ = os.path.splitext(base)
        matches = run_recognition(fpath)
        song = align_matches(self.sql, matches)
        confidence = song['CONFIDENCE']
        self.vprint(f"Confidence of a match: {confidence}.", "yellow")
        
        ### If there's an exact match, give feedback to user, otherwise if there's a possible match notify the user as well
        if confidence >= 400:
            self.vprint(f"EXACT MATCH FOUND FOR ID: {id_}, CHECK MATCHES.TXT", "green")
            with open("MATCHES.txt", "a") as f:
                f.write(f"{currentDate} {currentTime}: You've found an identical match with the database. Video with ID {id_} is an EXACT match, with a confidence of {confidence}!! Check it out at youtube.com/watch?v={id_}  !\n")
        elif confidence >= thresh:
            self.vprint(f"POSSIBLE MATCH FOUND FOR ID: {id_}, CHECK MATCHES.TXT", "green")
            with open("MATCHES.txt", "a") as f:
                f.write(f"{currentDate} {currentTime}: Video with YT ID {id_} has a possible match with the database, with a confidence of {confidence}! Check it out at youtube.com/watch?v={id_} !\n")
        
        return confidence >= thresh
    
    def get_videos(self):
        """
        Extract video ids and durations through yt-dlp
        """

        dir_here = os.path.abspath(os.getcwd())
        dir_yt_dlp_dir = os.path.join(dir_here, "yt-dlp")
        ### Set yt-dlp exectuable for windows and linux users
        if sys.platform == "win32":
            yt_dlp_exec = "yt-dlp.exe"
        else:
            yt_dlp_exec = "yt-dlp"
        path_yt_dlp_exec = os.path.join(dir_yt_dlp_dir, yt_dlp_exec)
        cmd = ["yt-dlp", "--sleep-requests 1", "--no-warnings", "--flat-playlist", "--print-to-file", "\"%(id)s %(duration)d\n%(title)s\"", "channel_video_urls.txt", f"{self.channel_url}"]
        print(' '.join(cmd))

        #Delete video urls txt file in case it still exists from a previous session
        try:
            os.remove("channel_video_urls.txt")
        except OSError:
            pass
        
        try:
            subprocess.check_output(' '.join(cmd))
            sleep(0.1)
            self.vprint(f"URLs gathered!")
        except KeyboardInterrupt:
            ### completely exit program if this is what user wants
            exit()
        except:
            ### always show error even when verbose is off
            cprint("Video URLs couldn't be gathered.", "red")
            return None

        # Construct and return a list of videos, where each video is a dict
        # containing the video id and video duration in seconds.
        video_ids, durations, titles = [],[],[]
        with open("channel_video_urls.txt", "r+", errors='replace') as f:
            for idx, x in enumerate(f, 1):
                if(idx % 2 == 1):
                    a = x.split()
                    if a[1] == "NA": continue
                    video_ids.append(a[0])
                    durations.append(int(a[1]))
                else: 
                    titles.append(x)

        # Delete video urls txt file afterwards
        try:
            os.remove("channel_video_urls.txt")
        except OSError:
            pass


        videos = []
        for (video_id, duration, title) in zip(video_ids, durations, titles):
            videos.append(
                {
                    "id" : video_id,
                    "duration" : duration,
                    "title" : title
                }
            )
        return videos
        
    def get_videos_html(self, source):
        """
        Extract video ids and durations from channel video page source
        """
        
        ### get video ids form page source.
        watch_expr = r'href="/watch\?v=([a-zA-Z0-9_-]+)"'
        matches = re.finditer(watch_expr, source)
        
        ### For each video, the id is put thrice in the page source, 
        ### so we have to use [::3] to grab only one of the ids
        video_ids = [match.groups()[0] for match in matches][::3]
        
        ### Get duration of video corresponding to each video id.
        soup = bs.BeautifulSoup(source, "html.parser")
        
        ### all time durations are contained within a tag with class
        ### "style-scope ytd-thumbnail-overlay-time-status-renderer"
        time_spans = soup.findAll(
            "span",
            {"class": "style-scope ytd-thumbnail-overlay-time-status-renderer"}
        )
        
        raw_durations = [ts.text.strip() for ts in time_spans[::2]]
        del time_spans
        
        ### Making video durations list
        durations = []
        for raw_duration in raw_durations:
            if raw_duration[0] not in "0123456789":
                continue
            time_units = raw_duration.split(":")
            seconds = int(time_units[-1])
            minutes = int(time_units[-2])
            hours = int(time_units[-3]) if len(time_units) > 2 else 0

            ### Get total duration in seconds.
            duration = seconds + (minutes * 60) + (hours * 3600)
            durations.append(duration)
        
        title_sp = soup.findAll(
            "yt-formatted-string", 
            {"id": "video-title"}
        )

        titles = [ts.text.strip() for ts in title_sp]
        del title_sp
        # Construct and return a list of videos, where each video is a dict
        # containing the video id, video duration in seconds and title.
        videos = []
        for (video_id, duration, title) in zip(video_ids, durations, titles):
            videos.append(
                {
                    "id" : video_id,
                    "duration" : duration,
                    "title" : title
                }
            )
        print(videos)
        return videos
        
        
        '''We may need to add also the video titles if we want to include a speedmode but for now this will do.'''
    
    
    def check_one_video(self, id_):
        song_fpath = self.get_song_mp3(id_)
        if song_fpath is None:
                return
        
        possible_match = self.check_file(song_fpath, )
        self.delete_mp3s()
        
        if possible_match:
            song_fname = os.path.split(song_fpath)[1]
            with open("MATCHES.txt", "a") as f:
                f.write(f"{currentDate} {currentTime}: {song_fname} with YT ID {id_} has a possible match with the database! Check it out!\n")
        else:
            self.vprint("Probably not a match.")
        
    
    
    def check_channel(self, min_duration, max_duration):
        if self.html_urls == True:
            #Get the HTML source of the channel's video section
            source = self.get_channel_source()
            videos = self.get_videos_html(source)
        else:
            videos = self.get_videos()
        
        #sort title arguments
        orSwitch = False
        if self.title != "":
            yesTitle, noTitle = [],[]
            if "+" in self.title: orSwitch = True
            temp_args = re.finditer(r"!?([\"\']).+?\1", self.title)
            titleargs = []
            for x in temp_args:
                titleargs.append(x.group(0))
            #print("titleargs: " + str(titleargs))
            titleargs = [x.strip("'\"\'") for x in titleargs]

            for x in titleargs:
                if re.match(r"^![\"\']", x):
                    noTitle.append(x[2:])
                else: yesTitle.append(x)


        target_videos = []
        for video in videos:
            if self.title != "":
                titleConflict = False
                titleMatch = False

                for x in yesTitle[:-1]:
                    titleMatch = x.lower() in video["title"].lower()
                    if not titleMatch and not orSwitch:
                        titleConflict = True
                        break
                    if orSwitch and titleMatch:
                        break
                for x in yesTitle[-1:]:
                    if x.lower() in video["title"].lower(): titleMatch = True
                    elif not titleMatch: titleConflict = True

                for x in noTitle:
                    if titleConflict: break
                    if x.lower() in video["title"].lower():
                        titleConflict = True
                        break

                if orSwitch and not titleConflict and not titleMatch:
                    titleConflict = True
                #print("titleConflict final + " + str(titleConflict))

                if titleConflict:
                    continue

            correctDuration =  video["duration"] >= min_duration and video["duration"] <= max_duration
            if ((self.ignore_checked == False and correctDuration) 
                or 
                (correctDuration and (self.ignore_checked == True and not self.sql.in_checked_ids(video["id"])))):
                target_videos.append(video)
        
        ### Get total number of videos to display progress percentage
        total_videos = len(target_videos)
        if total_videos == 0: self.vprint("All videos have been checked or are longer than than the maximum duration.","green"), exit()

        self.vprint("High confidence means a higher likelihood of the video being a match for the given song fingerprints.", "green")
        self.vprint("A confidence of 20 or more signifies a possible match, a confidence of 400 or more signifies an exact match.", "green")
        
        
        ### We use two indexes, both for a different purpose, _ is for progress percentage, 'index' is for getting correct slices of target_videos (so multithreading purposes)
        _ = 0
        for index in range(math.ceil(len(target_videos)/self.arguments.threads)):

            if total_videos - self.arguments.threads * (index) < self.arguments.threads: 
                section = target_videos[-(total_videos - self.arguments.threads * (index)):]
            else: section = target_videos[self.arguments.threads*index : self.arguments.threads*(index+1)]
            
            ### Downloading mp3 with multithreading
            jobs = []
            for video in section:
                id_ = video["id"]
                try:
                    self.vprint(f"Downloading audio from video with ID {id_}...")
                    thread = threading.Thread(target=self.get_song_mp3, args=(id_,))
                except KeyboardInterrupt:
                    self.delete_mp3s
                    exit()
                jobs.append(thread)

            for job in jobs:
                _ += 1
                job.start()
            for job in jobs:
                job.join()
            
            
            ### Fingerprinting with multithreading
            jobs = []
            for file in os.listdir("downloaded_mp3s"):
                p = ExcThread(target=self.check_file, args=(os.path.join("downloaded_mp3s", file), self.arguments.threshold, ))
                filename, file_extension = os.path.splitext(file)
                self.sql.add_checked_id(filename) #this should only happen if it's really checked
                jobs.append(p)
            
            for job in jobs:
                job.start()
            for job in jobs:
                try:
                    job.join()
                except (SystemExit, KeyboardInterrupt):
                    self.delete_mp3s()
                    sys.exit()
            
            self.vprint(f"{100*(_)/total_videos:.2f}% done with this channel/playlist")
            
            self.delete_mp3s()
            print("")    
        self.delete_mp3s()
    
    def main(self):
        if self.arguments.id is not None:
            self.check_one_video(self.arguments.id)
        elif self.arguments.url_file is not None or self.url_file is not None:
            try:
                now_time = tm.time()
                with open("urls.txt", "r") as c:
                    for x in c:
                        if self.verify_url(x):
                            self.channel_url = x
                            self.check_channel(min_duration = self.arguments.min_duration, max_duration = self.arguments.max_duration)
                            self.vprint(f"Duration of channel scan in seconds: {tm.time() - now_time}")
                            now_time = tm.time()
                    return
            except FileNotFoundError:
                cprint("Error: The file urls.txt was not found in this program's folder.", "red")
                exit()
        else:
            self.check_channel(min_duration = self.arguments.min_duration, max_duration = self.arguments.max_duration)
        
        self.vprint(f"Duration of channel scan in seconds: {tm.time() - start_time}")
        

def get_arguments():
    parser = argparse.ArgumentParser(description='''TMS-Finder''')
    
    parser.add_argument("-i", "--ignore", dest = "ignore", default=False, help="Ignore already checked videos", action='store_true')
    parser.add_argument("-s", "--speedmode", dest = "speedmode", help="Activate speed mode", action = "store_true")
    parser.add_argument("-v", "--verbose", dest = "verbose", help="Give Feedback, default = False", action = "store_true", default = False)
    parser.add_argument("-th", "--threshold", dest = "threshold", action="store", type = int, help = "Set the threshold for the number of hash matches at which you are notified of a match, default is 20", default = 20)
    parser.add_argument("-m", "--multi-threading", dest="threads", action="store",type=int, help="Amount of videos allowed to concurrently check, default is 1", default = 1)
    parser.add_argument("-c", "--channel", dest = "channel_url", help="Parse the channel url as command line argument")
    parser.add_argument("-uf", "--url-file", dest = "url_file", help = "Takes links from urls.txt to check multiple channels and playlists one after another.")
    parser.add_argument("-id" ,"--id", dest = "id", help = "Test a single video instead of a whole YT channel or playlist.")
    parser.add_argument("-r", "--restore-file", dest = "restore_file", help="Give a restore file to get the html source of a channel without opening the browser again")
    parser.add_argument("-t", "--title", dest = "title", help = "Use 'text' to set anything that must be part of the title, use !'text' to set anything that can't be part of the title, use one + if at least one 'text' has to match rather than all of them", default = "")
    parser.add_argument("-mnd", "--min-duration", dest = "min_duration", default = 0, type = int, help = "Set the min duration of videos of the videos that you want to check.")
    parser.add_argument("-mxd", "--max-duration", dest = "max_duration", default = 360000, type = int, help = "Set the max duration of videos of the videos that you want to check.")
    parser.add_argument("-html", "--html-urls", dest = "html_urls", help = "Force the alternative way of gathering urls and video durations through browser automation.", action = "store_true", default = False)

    return parser.parse_args()


if __name__ == '__main__':
    finder = Finder()
    finder.main()
