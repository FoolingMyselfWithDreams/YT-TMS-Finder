# YouTube TMS Finder

To find unidentified music on YouTube.

##
This is a continuation of the TMS Finder made by Ben-0-mad.
The text beyond the section "What you need to know" is mainly copied from the original with a couple of edits to reflect the new state of the code.

Please read the section on [How To Install](https://github.com/FoolingMyselfWithDreams/YT-TMS-Finder?tab=readme-ov-file#how-to-set-up-on-windows) and [General Usage](https://github.com/FoolingMyselfWithDreams/YT-TMS-Finder?tab=readme-ov-file#how-to-use) to get started.

Check out [Common Problems](https://github.com/FoolingMyselfWithDreams/YT-TMS-Finder?tab=readme-ov-file#common-problems) if you encounter any problems or errors.

See you somewhere!

--- FoolingMyselfWithDreams

### V1.0.5
Getting everything to a working state

New features:
- Check multiple channels (-uf option)
- Check playlists
- New and faster video URL gathering (browser automation gathering still available to use)
- Besides .mp3, accepts .flac and .wav files now
- User queries for easier usage
- Makes a copy of audio files, converts the copy to .mp3 with 320k bitrate and 44100 kHz sample rate to make the fingerprints always comparable (Fingerprinting audio files with
  different sample rates and bitrates than the audio on YouTube previously caused fingerprints to not correctly match with downloaded songs)
- More .bats
- Bug fixes

## What you need to know

This code was made in an effort to make it easier to find the song that has been dubbed 'The Most Mysterious Song on the Internet' as well as other unknown songs. This tool makes it possible to search YouTube channels for songs without having to manually check the videos.

This is done by gathering all video URLs of a YouTube channel or playlist, downloading a video, fingerprinting the audio, and checking it against a database (which is included in this program). It was developed for Windows so people don't have to install virtual machines or WSL subsystems or anything like that, and also because my university administrator doesn't allow changing operating systems. But it should work on Linux as well.

The necessary code was already available, I just made them work together.

## Credits & contributors:
- Credit to the makers of youtube-dl
- Special thanks and credit to Itspoma, the creator of the audio fingerprinting and recognition code.
- Thanks to nrsyed for helping with code optimisation.
- Thanks to Tamago-iku for contributing.
  
## How to use
### General usage:
- Double click # TMS Finder.bat and follow the instructions.
- To add more songs to the database, add .mp3, .wav or .flac audio files to the folder called "samples" and then open "# Collect Song Fingerprints.bat".
- Or use "# Reset Fingerprint Database.bat" to delete all songs from the database.
- "# Get Database Info" gives you more insight about the state of the database.

- In order to use the new URL file feature, add multiple channel or playlist links to the file called "urls.txt". The program will work through them one after another.


### Usage in cmd: 
```
find_stable.py [-h] [-i] [-s] [-v] [-t THRESHOLD] [-m THREADS] [-c CHANNEL_URL] [-uf ANY] [-id ID] [-r RESTORE_FILE] [-html]
```
1. ```-h``` for the help message
1. ```-i``` ignore videos that were checked in another session already
1. ```-s``` download only first 15 seconds of video. This speeds up the download and fingerprinting. [CAUTION: -s only makes sense to use if you know that you at least have the intro of a song fingerprinted, or if the intro musically is similar to parts of the rest of the song, and if you're only checking videos that have one song]
1. ```-v``` for verbosity / detailed messaging
1. ```-t``` to set the hash matches threshold (at which you will be notified of a match)
1. ```-m``` multithreading, max number of videos to check at the same time, 3 is optimal & recommended
1. ```-c``` to supply channel URL from command line, if this is not supplied, it will be asked automatically
1. ```-uf``` takes links from urls.txt to check multiple channels and playlists one after another
1. ```-id``` to check only one video ID
1. ```-r``` for restore file (This restore file has to be the html source of a youtube channel)
1. ```-mnd``` set the min duration in seconds of videos that you want to check
1. ```-mxd``` set the max duration in seconds of videos that you want to check
1. ```-html``` force the alternative way of gathering URLs and video durations through browser automation
   

**The restore file is automatically created after the first time you grab the HTML of a YouTube channel.**

Some unidentified music we find is different in BPM/pitch, therefore [this package](https://www.dropbox.com/s/ze3nzu8lecy6ndl/TMS%20subtle%20variants%20on%20tone%20and%20speed.zip?dl=0) with slightly different versions of TMS is available. Just put the files in the "mp3" folder and do ```python collect-fingerprints.py```.

## How to set up on Windows

1. Install any program that opens .zip files like WinRar, WinZip, 7-Zip or any of the other available .zip programs.
2. Find the newest release of TMS Finder by clicking [here](https://github.com/FoolingMyselfWithDreams/YT-TMS-Finder/releases). You can download it by clicking on "Source code (zip)" on the bottom.
3. Extract the file (right click .zip file and click "Extract here"). This puts all the TMS Finder files in a new folder which is named YT-TMS-Finder-"Version Number".
4. Go to the YT-TMS-Finder folder.
   Please make sure that the folder path doesn't have any of the following characters: ```@ $ % & \ / : * ? " ' < > | ~ ` # ^ + = { } [ ] () ; !```
   For example, if your folder path would be C:\Users\Admin\@Downloads\YT-TMS-Finder-1.0.5(2)\YT-TMS-Finder-1.0.5, then you would have to rename it to C:\Users\Admin\Downloads\YT-TMS-Finder-1.0.5\YT-TMS-Finder-1.0.5, removing @ and ().
   If for some reason you can't rename any problematic folders, move on to the [Alternative Installation](https://github.com/FoolingMyselfWithDreams/YT-TMS-Finder/edit/master/README.md#alternative-installation-process)
5. Right-click on Install.bat and choose "Run as Administrator".
6. If it says "Python is not being recognised as an internal command", please have a look at [this](https://github.com/FoolingMyselfWithDreams/YT-TMS-Finder?tab=readme-ov-file#python-is-not-being-recognised-as-an-internal-command).
7. If you had any problems with installing PyAudio, click [here](https://github.com/FoolingMyselfWithDreams/YT-TMS-Finder/edit/master/README.md#pyaudio-errors).
8. Now double click on "# TMS Finder" inside the YT-TMS-Finder folder and follow the instructions.
9. If you see any errors, please have a look at the [Common Problems section](https://github.com/FoolingMyselfWithDreams/YT-TMS-Finder/edit/master/README.md#common-problems).
10. Check for any matches! They will be displayed inside a file called "MATCHES.txt" which will be created in the folder so you don't have to check the progress constantly. If any videos get missed, they'll be logged in "missed.txt" as well.


### Alternative Installation Process:

1. Make sure you have [Python 3](https://www.python.org/downloads/) installed. Click "Add Python to your PATH" during the install.
2. Install any of the programs that opens .zip files.
3. Find the newest release of TMS Finder by clicking [here](https://github.com/FoolingMyselfWithDreams/YT-TMS-Finder/releases). You can download it by clicking on "Source code (zip)" on the bottom.
4. Extract the file (right click .zip file and click "Extract here"). This puts all the TMS Finder files in a new folder which is named YT-TMS-Finder-"Version Number".
5. Open a command prompt (Press Windows Key, search for CMD) and install the requirements by typing:
```
cd "insert folder path to the requirements.txt file" (without quotes)
```
press Enter and then:
```
pip install -r requirements.txt
```
If it says "Python is not being recognised as an internal command", please have a look at [this](https://github.com/FoolingMyselfWithDreams/YT-TMS-Finder?tab=readme-ov-file#python-is-not-being-recognised-as-an-internal-command).

6. If you have problems installing PyAudio, move on to 7. for now.

7. To make the installation easier, we'll use chocolatey which is just like brew, pip, or other module utilities. Press the Windows Key, search for CMD, right click on CMD and choose to open it in Administrator mode, copy & paste this command and press Enter:
```
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command " [System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin" 
```

8. Great! Now you have Chocolately installed. Next we'll install the chromedriver and bs4 (Beautiful Soup). If you already have the chromedriver you can skip this step. Close the previous CMD window and open a new CMD in administrator mode, then run:
``` 
choco install chromedriver -y
```

9. In order to download audio from YouTube we'll need ffmpeg. We'll download this as well. If you already have ffmpeg you can skip this step. In the same CMD window, run:
``` 
choco install ffmpeg -y
```

10. If you had any problems with installing PyAudio, that's a common issue. The solution to downloading PyAudio if the normal ```pip install pyaudio``` fails, is this:
- Go to https://pypi.org/project/PyAudio/#files and download the .whl file for your version of Python.
Then open up a command prompt (press Windows key and type CMD). Navigate to the folder with the .whl file (cd "insert folder path" (without the quotes)) and do ```pip install PyAudio-0.2.14-cp312-cp312-win_amd64.whl``` or whatever .whl file suits your version of Python. Now you have it installed.

11. Now double click on "# TMS Finder" or type the following into CMD and press Enter: ```python find_stable.py```

12. Check for any matches! They will be displayed inside a file called "MATCHES.txt" which will be created in the folder so you don't have to check the progress constantly. If any videos get missed, they'll be logged in "missed.txt" as well.


## How to set up on Linux

1. Make sure you have [Python 3](https://www.python.org/downloads/) installed. Click "Add Python to your PATH" during the install.
1. Open a terminal and install the requirements:
```
$ pip install -r requirements.txt
```
3. Do you have problems installing PyAudio? Please skip to the next step.

4. Installing ffmpeg:
```
sudo apt install software-properties-common
sudo apt update
sudo add-apt-repository ppa:jonathonf/ffmpeg-4
sudo apt install ffmpeg
```

5. In case you have any problems with installing PyAudio, please check out [this](https://stackoverflow.com/questions/20023131/cannot-install-pyaudio-gcc-error)

6. To install the chromedriver on Linux: please go see [here](https://makandracards.com/makandra/29465-install-chromedriver-on-linux)

7. Then do: ```python find_stable.py```


## Note

- In case you do ```python reset-database.py```, simply do ```python collect-fingerprints.py```.
- verbosity update and speedmode update coming soon.

## Updates

### V1.0.5
Getting everything to a working state

New features:
- Check multiple channels (-uf option)
- Check playlists
- New video URL gathering (browser automation gathering still available to use)
- Accepts .flac and .wav files now
- User queries for easier usage
- Makes a copy of audio files, converts the copy to .mp3 with 320k bitrate and 44100 kHz sample rate to make the fingerprints always comparable (Fingerprinting audio files with
  different sample rates and bitrates than the audio on YouTube previously caused fingerprints to not correctly match with downloaded songs)
- More .bats
- Bug fixes

### V1.0.4

### V1.0.4-beta
- Added multithreading

### V1.0.4-alpha.1/2
- Made it easier for the user to get the chromedriver.exe for selenium right
- Added -r option for restore file (html source of a youtube channel)
- Added -id option to check only one video
- Added -t option to select the hash matches threshold yourself, default is 20.
- Colorama RecursionError was fixed.

### V1.0.4-alpha
- Code optimisation

### V1.0.3
- Speedmode: use ```-s``` (it uses only the first 30 seconds of a video to do the audio recognition on)
- Verbosity: use ```-v``` (recommended)
- Now tells you how far the progress is.
- Bug fixes.

### V1.0.2
- Channel url can now also be given as command line argument (supply ```-c CHANNEL_URL```)

### V1.0.1
- Option to ignore previously tried videos. This is useful in case the process unexpectedly ends and you want to continue where you left off.
- Speedmode available in v1.0.3

### V1.0.1-alpha.1
- Bug fix

## Example output

```
C:\Users\username> python find_stable.py
Welcome to...

__   _______   ________  ___ _____  ______ _           _
\ \ / /_   _| |_   _|  \/  |/  ___| |  ___(_)         | |
 \ V /  | |     | | | .  . |\ `--.  | |_   _ _ __   __| | ___ _ __
  \ /   | |     | | | |\/| | `--. \ |  _| | | '_ \ / _` |/ _ \ '__|
  | |   | |     | | | |  | |/\__/ / | |   | | | | | (_| |  __/ |
  \_/   \_/     \_/ \_|  |_/\____/  \_|   |_|_| |_|\__,_|\___|_|


Enter a channel URL to begin.
Example URL:  https://www.youtube.com/channel/UCmSynKP6bHIlBqzBDpCeQPA/videos

DevTools listening on ws://127.0.0.1:36749/devtools/browser/c974ddad-0534-4ee7-9f82-50c47379fae2

Downloading audio from video with ID lI0kLA-7J5Q...
Audio downloaded! Performing fingerprint match scan...
Confidence of a match: 8.
1.92% done

Downloading audio from video with ID RpnhkS_Stfs...
Audio downloaded! Performing fingerprint match scan...
Confidence of a match: 12.
3.85% done

Downloading audio from video with ID -JRSeiogFbA...
Audio downloaded! Performing fingerprint match scan...
Confidence of a match: 8.
5.77% done
```

## Common problems
1. ### Python is not being recognised as an internal command.
    FIX by adding Python.exe folder to the PATH variable. It's possible to do this through the Python installer.
    
    On Windows, you can also do this by doing this:
    
    - Press the Windows Key, search for "Variables" or "Path". 
    - Click on the option that says System Environment Variable. 
    - Once you did, click on the button that says Environment Variables which is on the very bottom of the window. Double click on "Path" in the top section, click on the button "New" in the top right. 
    - Copy & Paste the folder path that has python.exe in it. 
      For example, this folder could be called

      C:\Users\PC\AppData\Local\Programs\Python\Python312\  
    - Additionally, add the folder Scripts which you can find in the same folder as python.exe 
      For example, this folder could be called

      C:\Users\PC\AppData\Local\Programs\Python\Python312\Scripts
    - If everything went well, you should have successfully added Python to PATH now and the error should disappear.
    
    It still says "Python is not being recognised as an internal command" ?
    
    Press the Windows key and type in app alias, open the one below PC Settings.
    This list might contain multiple python.exe, try disabling all but one and try this with every        single one until you find the one that makes the error disappear.

2. ### Problem with Selenium and chromedriver.
   For Windows please do step 3 and 4 of the setup!

3. ### Problem with ffmpeg.
   Install ffmpeg in step 6.
   
4. ### Error: Song Database likely empty
   Move .mp3, .wav or .flac files to the folder "samples" and open # Collect Fingerprints.

5. ### [Errno 13] Permission denied
   This could have multiple reasons.
   Usually this error means that Windows is set up in a way that doesn't allow the program access to the other files in the folder.
   - Try right clicking the TMS Finder folder, click on Properties, then onto the Security tab.
   - Click on Users, then the Edit button on the right side. Now select Users again.
   - The program needs at least the following permissions: Modify, Read & execute, Read, and Write.
   You could also pick Full Control and give the program all permissions that way.

   If that still doesn't help, you might have to do this for every .bat file in the folder.

   Often this error happens because your Windows user account isn't automatically set to have Admin rights. You may want to look up on how to do change this to avoid this type of error in the future entirely.
   
   Your antivirus or firewall could also be blocking the program.

6. ### PyAudio errors
   If you had any problems with installing PyAudio, that's a common issue. The solution to downloading PyAudio if the normal install fails, is this:
   Go to https://pypi.org/project/PyAudio/#files and download the .whl file for your version of Python.
   Then open up a command prompt (press Windows key and type CMD). Navigate to the folder with the .whl file (type this into the CMD window:  cd "insert folder path" (without the quotes)), press Enter and then
   type this in and press Enter: ```pip install PyAudio-0.2.14-cp312-cp312-win_amd64.whl``` or whatever .whl file suits your version of Python. Now you have it installed.

## Contributing

If you'd like to contribute, these are the things that still need to be done:
- Use yt-dlp python module instead of actual yt-dlp.exe file. This allows us to remove the yt-dlp folder in this repo.
- Finish FAQ section in this readme
- Create and test setup file for Windows and Linux to make installation quicker.
- Make it easier to get started (Python installation etc.)
- Automatically create and fingerprint versions of audio files with different pitch
- Download .m4a audio directly rather than download video and extract audio.
  I already do this with files that have the wrong format, but this could be added in general since comparing .mp3 with .m4a fingerprint hashes seems to work fine (needs additional tests though)
- Create a simple GUI?
- Test more on Linux
- More pictures?

## FAQ
- **How to check a YouTube channel?**

  ```
  > python find_stable.py -c CHANNEL_ID
  ```
- **Can I add my own songs to the database?**

  Yes, itspoma made this possible. Just upload that mp3 file into the "mp3" folder. Now do `python collect-fingerprints.py`. Any song in the 'mp3' folder that was previously added already will be skipped. The song is now added into the database and can be recognised. For more info please check out [itspoma's repo](https://github.com/itspoma/audio-fingerprint-identifying-python).
  
- **Is it storage efficient?**
  
  After installing the necessary modules, yes. The bot automatically deletes mp3 files after they have been checked against the database.

- **What is the optimal number of threads?**
  
  After doing a couple of quick tests, I got these results:
  
  * \# of threads = 1: 12 videos took 98.53 seconds
  * \# of threads = 2: 12 videos took 57.15 seconds
  * \# of threads = 3: 12 videos took 50.21 seconds
  * \# of threads = 4: 12 videos took 51.58 seconds
  * \# of threads = 5: 12 videos took 55.09 seconds
  
  Therefore it seems like 3 threads is a good option. And after doing some tests with a larger number of videos, I got these results:
  [To be finished]

- **How does it work in detail?**
  
  First we have to get all the video IDs from a YouTube channel. This is not possible by simply using requests or beautifulsoup. We would have to open the browser ourselves going down all the way to the bottom of the page, but we can also do this with a webbot so we don't have to do it ourselves.
  
  Then it downloads the HTML source. From this HTML file we can obtain all the video IDs and their time length without the need of the YouTube API (which costs money). For every video the following is done:
  1. Download the audio from the video in mp3 format using yt-dlp.
  2. Fingerprint the song.
  3. Match the fingerprint against the database.
  4. If there are more than 100 hashes that match, print this on the screen and add it to a "MATCHES.txt" file.
