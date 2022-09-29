#Enable static_mode to try the app without a connection to a Bluesound player.
static_mode_conf = False

#Replace the part "192.168.190.10" with the ip-adress of your Bluesound player. 
#You can find the ip adress of your player in the official APP under Help and then Diagnostics
base_url_conf = "http://192.168.86.28:11000/"

#If you want to use the app on Windows, replace this with the drive letter of 
#your network shared music-folder.
windows_path_conf = "C:\Python"

#If you want to use the app on Linux (like Raspbian on an Raspberry pi), 
#replace this with the path of your network shared music-folder.
linux_path_conf = "/mnt/mynas/"

#The network share as used in the official Bluesound app
bluesound_path_conf = "//mynas/music/"

#The network share as found in the status.xml
#Find this in your browser by opening [ip adress of player]:11000/Status
#The needed line is found in the fn-tag of the Status.xml file
#The line is also found in the official APP under Help and then Diagnostics,
#but then leave the 'tmp' part away and put a '/' at the end
bluesound_path2_conf = "/var/mnt/mynas-music/"

#Insert your last-fm api key if you want to use their online album art.
last_fm_api_key_conf = ""
