# BluePi #
BluePi is based of the core Bluebox functions which interface to a BluOS device. It was developed so that the following information can be displayed on an always on display powered by a Raspberry Pi:
- Album art
- Artist and song information
- Volume Overlay
The aim was to create a screen for BluOS devices that don't have a display, such as the Bluesound Node/Powernode, akin to the the NAD M10/M33.

It runs on Windows and a Raspberry Pi running Raspbian (Linux). It was tested on the following equipment

* Bluesound Powernode (2021) integrated amplifier.
* Raspberry Pi 3B
* Pimoroni HyperPixel 4.0 Square Non-Touch 

# Screenshot #



# Installation #

## Files ##
The program consists of two main files. The file app_logic.py contains command-functions and status-lookup functions that can be reusable in other projects. The other file blupi.py is mainly the GUI. The configuration is done in app_conf.py. 

## Run it on Windows and a Raspberry Pi ##
The Bluebox app is written in Python 3. I have mine running on three devices: Windows and two Raspberry Pi's running Raspbian (Linux).

