import platform
import os
import urllib.request
import time
import csv
import threading
from xml.dom import minidom
from datetime import datetime, timedelta
import datetime as dt
import random
from PIL import Image, ImageTk

from app_conf import *

static_mode = static_mode_conf

if static_mode is False:
    base_url = base_url_conf
    if platform.system() == 'Windows':
        path = windows_path_conf
        plG_length = 10
    if platform.system() == "Linux":
        path = linux_path_conf
        plG_length = 11
if static_mode is True:
    base_url = "file:"
    path = ""
    plG_length = 10

last_fm_api_key = last_fm_api_key_conf

class Status(object):
    def __init__(self, interval=0.5):
        self._interval = interval
        self._last_update = None
        self.status_parsed = None
        print("Status() initialized at " + str(dt.datetime.now()))

    def _update_status(self):
        if (self._last_update is None) or ((dt.datetime.now() - self._last_update).total_seconds() > self._interval):
            self.status_xml = urllib.request.urlopen(base_url + "Status")
            self.status_parsed = minidom.parse(self.status_xml)
            self._last_update = dt.datetime.now()

    def get_status(self):
        self._update_status()
        return self.status_parsed

    def get_status(self):
        """Returns most recent status."""
        self._update_status()
        return self.status_parsed

    def mp3_on(self):
        try:
            status_elements = self.get_status().getElementsByTagName("service")[0]
            service = status_elements.firstChild.data
            if service == "LocalMusic":
                return True
            else:
                return False  
        except IndexError as error:
            return False
      
    def radio_on(self):
        try:
            status_elements = self.get_status().getElementsByTagName("canSeek")[0]
            canSeek = status_elements.firstChild.data
            if canSeek == "0":
                return True
            else:
                return False  
        except IndexError as error:
            return False

    def spotify_on(self):
        try:
            status_elements = self.get_status().getElementsByTagName("service")[0]
            service = status_elements.firstChild.data
            if service == "Spotify":
                return True
            else:
                return False  
        except IndexError as error:
            return False

    def check_quality(self):
        try:
            status_elements = self.get_status().getElementsByTagName("quality")[0]
            quality = status_elements.firstChild.data
            try:
                quality = int(quality) / 1000
                return str(int(quality))
            except ValueError as error:
                if quality == "cd":
                    return "FLAC"
                else:
                    return quality    
        except IndexError as error:
            return "Error"

    def check_repeat(self):
        try:
            status_elements = self.get_status().getElementsByTagName("repeat")[0]
            repeat = status_elements.firstChild.data
            if repeat == "0":
                return "ON"
            if repeat == "1":
                return "1"
            if repeat == "2":
                return "OFF"
        except IndexError as error:
            return ""

    def check_shuffle(self):
        if self.mp3_on() is True:
            status_elements = self.get_status().getElementsByTagName("shuffle")[0]
            shuffle = status_elements.firstChild.data
            if shuffle == "0":
                return "OFF"
            if shuffle == "1":
                return "ON"
        else:
            return ""

    def check_totlen(self):
        try:
            status_elements = self.get_status().getElementsByTagName("totlen")[0]
            totlen = status_elements.firstChild.data
            totlen = float(totlen)
            return int(totlen)
        except IndexError as error:
            return 0

    def check_totlen_converted(self):
        try:
            tmp = timedelta(seconds=int(self.check_totlen()))
            time_total = datetime(1,1,1) + tmp
            if int(self.check_totlen()) >= 3600:
                return "%d:%d:%d" % (time_total.hour, time_total.minute, time_total.second)
            else: return "%d:%d" % (time_total.minute, time_total.second)
        except IndexError as error:
            return "0"

    def check_progress(self):
        if static_mode is True:
            return random.randint(0,120)
        else:
            try:
                status_elements = self.get_status().getElementsByTagName("secs")[0]
                secs = status_elements.firstChild.data
                return int(secs)
            except IndexError as error:
                return 0

    def check_progress_converted(self):
        try:
            tmp = timedelta(seconds=int(self.check_progress()))
            progress = datetime(1,1,1) + tmp
            if int(self.check_progress()) >= 3600:
                return "%d:%d:%d" % (progress.hour, progress.minute, progress.second)
            else: return "%d:%d" % (progress.minute, progress.second)
        except IndexError as error:
            return "0"

    def check_rel_progress(self):
        try:
            if self.check_totlen() == 0:
                return 0
            else:
                rel_progress = self.check_progress() / self.check_totlen() * 1000
                return rel_progress
        except IndexError as error:
            return 0

    def check_playing_dir_and_file(self):
        try:
            status_elements = self.get_status().getElementsByTagName("fn")[0]
            playing_dir_and_file = status_elements.firstChild.data
            playing_dir_and_file = playing_dir_and_file.replace(bluesound_path2_conf, "")
            return playing_dir_and_file
        except IndexError as error:
            return ""

    def check_songname(self):        
        try:
            status_elements = self.get_status().getElementsByTagName("title1")[0]
            title1 = status_elements.firstChild.data
            return title1
        except IndexError as error:
            return ""

    def check_artist(self): 
        try:
            status_elements = self.get_status().getElementsByTagName("artist")[0]
            artist = status_elements.firstChild.data
            return artist
        except IndexError as error:
            return ""

    def check_album(self):        
        try:
            status_elements = self.get_status().getElementsByTagName("album")[0]
            album = status_elements.firstChild.data
            return album
        except IndexError as error:
            return ""

    def check_state(self):        
        try:
            status_elements = self.get_status().getElementsByTagName("state")[0]
            state = status_elements.firstChild.data
            return state
        except IndexError as error:
            return ""

    def check_volume(self):        
        try:
            status_elements = self.get_status().getElementsByTagName("volume")[0]
            volume = status_elements.firstChild.data
            return volume
        except IndexError as error:
            return ""

    def check_radiostation(self):        
        try:
            status_elements = self.get_status().getElementsByTagName("title1")[0]
            radiostation = status_elements.firstChild.data
            return str(radiostation)
        except IndexError as error:
            return ""

    def check_radio_title_playing(self):        
        try:
            status_elements = self.get_status().getElementsByTagName("title2")[0]
            title2 = status_elements.firstChild.data
            return str(title2)
        except IndexError as error:
            return ""

    def check_spotify_title21_playing(self):        
        try:
            status_elements = self.get_status().getElementsByTagName("title2")[0]
            title2 = status_elements.firstChild.data
            status_elements = self.get_status().getElementsByTagName("title1")[0]
            title1 = status_elements.firstChild.data
            return str(title2 + " - " + title1)
        except IndexError as error:
            return ""

class Playlist(object):
    def __init__(self, status, interval=0.5):
        self._interval = interval
        self._last_update = None
        self.status = status
        print("Playlist() initialized at " + str(dt.datetime.now()))

    def _update_playlist(self):
        if (self._last_update is None) or ((dt.datetime.now() - self._last_update).total_seconds() > self._interval):
            if static_mode is True:
                self.playlist_xml = urllib.request.urlopen(base_url + "Playlist")
            else:
                self.playlist_xml = urllib.request.urlopen(base_url + "Playlist?start=0&end=800")
            self.playlist_parsed = minidom.parse(self.playlist_xml)
            self._last_update = dt.datetime.now()

    def get_playlist(self):
        """Returns most recent status."""
        self._update_playlist()
        return self.playlist_parsed

    def check_playlist(self):
        self.playlist = []
        if self.status.mp3_on() is True:
            self.songs = self.get_playlist().getElementsByTagName("song")
            for song in self.songs:
                self.songid = song.getAttribute("id")
                self.title = song.getElementsByTagName("title")[0]
                self.art = song.getElementsByTagName("art")[0]

                if self.art.firstChild.data == "Unknown Artist" or self.art.firstChild.data == "Various":
                    self.playlist.append(self.title.firstChild.data)
                else:
                    self.playlist.append(self.art.firstChild.data + " - " + self.title.firstChild.data)
        
        if self.status.radio_on() is True:
            self.playlist.append(self.status.check_radio_title_playing())

        if self.status.spotify_on() is True:
            self.playlist.append(self.status.check_spotify_title21_playing())

        return self.playlist

    def check_songid(self):
        self.song_id = 1
        if self.status.mp3_on() is True:
            self.status_elements = self.status.get_status().getElementsByTagName("song")[0]
            self.song_id = self.status_elements.firstChild.data
        return int(self.song_id)

class Keyb_input_processor(object):
    def __init__(self, keyb_input, status, control):
        print("app_logic krijgt " + keyb_input)
        
        if len(keyb_input) == 1:
            Keyb_control(keyb_input, status, control)

        elif keyb_input.startswith ("0"):
            keyb_input = (keyb_input[1:])
            Bluesound_radio(keyb_input)

        elif keyb_input.startswith ("-"):
            keyb_input = (keyb_input[1:])
            Bluesound_goto_specified_playlist_position(keyb_input)

        else:
            Bluesound_play_dir(keyb_input)
    
class Bluesound_play_dir(object):
    def __init__(self, keyb_input):
        
        no_clear = 0
        shuffle_on = 0
        if keyb_input.startswith ("+"):
            no_clear = 1
            keyb_input = (keyb_input[1:])
        if keyb_input[0].isdigit():
            keyb_input = keyb_input + " "
        output_os_walk=[] # maakt lijst leeg
        for root, dirs, files in os.walk(path):
            if keyb_input.lower() in root.lower() and "@eaDir" not in root:
                output_os_walk.append(root) # zet alle roots met asked-number in de lijst
        
        found_dir = "" # Leeg maken, zodat je later kunt checken of de dir wel gevonden is

        try: found_dir = (output_os_walk[0]) # de root met asked-number op positie 0 is de juiste
        except IndexError as error:
            print("Deze lijst bestaat niet.")
            return None # slaat de rest van de functie over en gaat terug naar de hoofdloop

        found_dir_converted = found_dir.replace(" ", "%20")
        found_dir_converted = found_dir_converted.replace("&", "%26")
        found_dir_converted = found_dir_converted.replace(path, bluesound_path_conf) # het pad zoals de Bluesound netwerkspeler die herkent
        found_dir_converted = found_dir_converted.replace("\\", "/")
        print(base_url + "Add?service=LocalMusic&playnow=-1&path=" + found_dir_converted)
            
        if no_clear == 0:
            urllib.request.urlopen(base_url + "Clear")
        time.sleep(.100)

        with urllib.request.urlopen(base_url + "Add?service=LocalMusic&playnow=-1&path=" + found_dir_converted) as feedback:
            print(feedback.read(5000))
        time.sleep(.100)
        
        if os.path.exists(found_dir + "/!shuffle_on.txt"):
            shuffle_on = 1
        
        if shuffle_on == 0:
            urllib.request.urlopen(base_url + "Shuffle?state=0") # state 0 is geen shuffel; state 1 is shuffel
        if shuffle_on == 1:
            urllib.request.urlopen(base_url + "Shuffle?state=1") # state 0 is geen shuffel; state 1 is shuffel
            time.sleep(.100)
            urllib.request.urlopen(base_url + "Skip")

        time.sleep(.100)                
        urllib.request.urlopen(base_url + "Repeat?state=0") # state 0 is repeat all; state2 is niet repeat

class Control(object):
    def __init__(self, status):
        self.status = status

    def previous(self): # prevous
        urllib.request.urlopen(base_url + "Back")

    def next(self): # next
        urllib.request.urlopen(base_url + "Skip")

    def stop(self): # Stop
        urllib.request.urlopen(base_url + "Stop")

    def pause(self): # Pause
        print("pauzeopdracht")
        urllib.request.urlopen(base_url + "Pause")

    def play(self): # Play
        urllib.request.urlopen(base_url + "Play")

    def repeattoggle(self): # repeat toggle
        repeatstatus = self.status.check_repeat()
        if repeatstatus == "ON":
            repeatstatus = "2"
        elif repeatstatus == "OFF":
            repeatstatus = "0"
        else:
            repeatstatus = "0"
        urllib.request.urlopen(base_url + "Repeat?state=" + repeatstatus)

    def repeaton(self): # repeat on
        urllib.request.urlopen(base_url + "Repeat?state=0")

    def repeatoff(self): # repeat off
        urllib.request.urlopen(base_url + "Repeat?state=2")

    def shuffleon(self): # shuffle off
        urllib.request.urlopen(base_url + "Shuffle?state=0")

    def shuffleoff(self): # shuffle on
        urllib.request.urlopen(base_url + "Shuffle?state=1")

    def seekbackward(self): # seek 30 sec backward
        secs = self.status.check_progress()
        secs = int(secs) - 30
        if secs < 0:
            secs = 0
        urllib.request.urlopen(base_url + "Play?seek="+ str(secs))

    def seekforward(self): # seek 30 sec forward
        secs = self.status.check_progress()
        maxsecs = self.status.check_totlen()
        secs = int(secs) + 30
        if secs < 0:
            secs = 0
        if secs > maxsecs:
            secs = maxsecs - 5
        urllib.request.urlopen(base_url + "Play?seek="+ str(secs))

class Keyb_control(object):
    def __init__(self, keyb_input, status, control):
        self.control = control

        if keyb_input == "4": # previous track
            urllib.request.urlopen(base_url + "Back")
  
        if keyb_input == "6": # next track
            urllib.request.urlopen(base_url + "Skip")
    
        if keyb_input == "0": # Stop
            urllib.request.urlopen(base_url + "Stop")

        if keyb_input == "3": # Play
            urllib.request.urlopen(base_url + "Play")
    
        if keyb_input == "8": # repeat on
            urllib.request.urlopen(base_url + "Repeat?state=0")
    
        if keyb_input == "1": # repeat off
            urllib.request.urlopen(base_url + "Repeat?state=2")
    
        if keyb_input == "2": # shuffle off
            urllib.request.urlopen(base_url + "Shuffle?state=0")
    
        if keyb_input == "5": # repeat on
            urllib.request.urlopen(base_url + "Shuffle?state=1")
    
        if keyb_input == "7": # seek 30 sec back
            self.control.seekbackward()
            
        if keyb_input == "9": # seek 30 sec forward
            self.control.seekforward()

class Bluesound_goto_specified_playlist_position(object):
    def __init__(self, keyb_input):
        keyb_input = int(keyb_input) -1
        keyb_input = str(keyb_input)
        urllib.request.urlopen(base_url + "Play?id=" + keyb_input)

class Bluesound_radio(object):
    def __init__(self, keyb_input):
        radio_dict = {}
        with open(path + 'radio.csv', 'r') as f:
            data = csv.DictReader(f, delimiter=',')
            for row in data:
                item = radio_dict.get(row["NR"], dict())
                item[row["NR"]+"-STATION"] = str(row["STATION"])
                item[row["NR"]+"-URL"] = str(row["URL"])
                radio_dict[row["NR"]] = item
        try: 
            radio_station = (radio_dict[keyb_input][keyb_input+"-STATION"])
            radio_url = (radio_dict[keyb_input][keyb_input+"-URL"])
            print("Speel Radio " + radio_station + " via " + radio_url)
        except KeyError as error:
            print("Dit radiostation bestaat niet.")
            return None
        
        with urllib.request.urlopen(base_url + "Play?url=" + radio_url) as feedback:
            print()

class Albumart(object):
    def __init__(self, status):
        self.status = status

    def return_image_link(self):
        if self.player_img_link() != False and self.recognize_grey_image() != True:
            return self.player_img_link()
        elif self.replace_with_lastfm() != False:
            return self.replace_with_lastfm()
        elif self.replace_with_coverart_from_dir() != False:
            return self.replace_with_coverart_from_dir()
        elif self.fallback_image != False:
            return self.fallback_image()
        else:
            return False

    def player_img_link(self):
        xml_image_element = "image"
        if self.status.spotify_on() is True:
            xml_image_element = "currentImage"

        try:
            status_elements = self.status.get_status().getElementsByTagName(xml_image_element)[0]
            playing_image_location = status_elements.firstChild.data
            if playing_image_location.startswith ("/"):
                playing_image_location = (playing_image_location[1:])
                playing_image_location = base_url + str(playing_image_location)
                return playing_image_location
            else:
                return playing_image_location
        except IndexError as error:
            return False

    def recognize_grey_image(self):
        self.greyimage = False
        img = "1"
        imggrijs = "2"
        try: 
            img = Image.open(urllib.request.urlopen(self.player_img_link()))
        except AttributeError as error:
                return False
        if os.path.exists(path + "APP_images/standaard_grijs_met__lichtgrijze_muzieknoot.jpg"):
            imggrijs = Image.open(path + "APP_images/standaard_grijs_met__lichtgrijze_muzieknoot.jpg")
        if img == imggrijs:
            self.greyimage = True
        try:
            img.close()
        except AttributeError as error:
            None
        try:
            imggrijs.close()
        except AttributeError as error:
            None
        return self.greyimage

    def replace_with_lastfm(self):
        artist = self.status.check_artist()
        track = self.status.check_songname()
        if artist == "":
            artist_and_track = self.status.check_radio_title_playing()
            artist_and_track_splited = artist_and_track.split(" - ")
            try: 
                artist = artist_and_track_splited[0]
                track = artist_and_track_splited[1]
            except IndexError as error:
                return False            
            print(track + " by " + artist)
        try:
            self.lastfm_xml = urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" 
                    + last_fm_api_key
                    + "&artist=" + artist 
                    + "&track=" + track)
        except urllib.error.HTTPError as error:
            return False
        try:
            self.lastfm_parsed = minidom.parse(self.lastfm_xml)
            lastfm_elements = self.lastfm_parsed.getElementsByTagName("image")[2]
            self.lastfm_image_link = lastfm_elements.childNodes[0].data
            return self.lastfm_image_link
        except IndexError as error:
            return False

    def replace_with_coverart_from_dir(self):
        dir_incl_file = self.status.check_playing_dir_and_file()
        dir_excl_file = os.path.dirname(dir_incl_file) 
        if os.path.exists(path + dir_excl_file + "/Coverart.jpg"):
            playing_image_location = path + dir_excl_file + "/Coverart.jpg"
            return playing_image_location
        else:
            return False

    def fallback_image(self):
        if os.path.exists(path + "APP_images/music.png"):
            return path + "APP_images/music.png"
        else:
            return False



