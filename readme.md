# Bluebox #
Bluebox is an alternatieve app to control the Bluesound Node music player. It's name comes from Bluesound and Jukebox. It runs on Windows and a Raspberry Pi running Raspbian (Linux). The Bluebox app doesn't make use of ID3 tags like artist and album. It's purely folder based.

# Screenshot #
![GUI image](https://tweakers.net/ext/f/Kpma7dO1jsqwgu0KFJbyTHXK/full.png)

# Purpose #
I wanted a few things the offical Bluesound app does not offer:
* Run it on (Windows and) a Raspberry Pi
* Physical buttons for control 
* A physical display, permanently showing the playlist and album art
* Quick access to unlimited music directories and unlimited radio stations
* By starting some music, automatically clear the playlist and load the whole directory
* The app shouldn't have to update if you update your Bluesound music index
* Get album art from multiple sources like Last fm

# Usage #

## Physical buttons for control ##
The Bluebox app, running on a Raspberry Pi, can be controlled by a physical numeric keypad. Like this:
![Keypad image](https://tweakers.net/ext/f/Bp6pbeOblb8KT7XEZi70ZIwm/medium.jpg)

## Basic play functions ##
The Bluebox app has some buttons like play and pause. Personally I don't use them. I only use the numeric keypad. 

After each command, you press enter.

```
Play: 3
Pause: 0
Next: 6 (arrow right)
Previous: 4 (arrow left)
Seek 30 sec forward: 9 (above arrow right)
Seek 30 sec backward: 7 (above arrow left)
Repeat on: 8 (endless sign)
Repeat off: 1
Shuffle on: 5
Shuffle off: 2
Goto number 11 of the playlist: -11
Start playing album 123 without clearing playlist: +132
```

When you start playing a music folder, repeat is automaticcaly on and shuffle is automatically off. This is different when there is an empty file "!shuffle_on" in the music directory.

## Start playing a music folder ##
The Bluebox app doesn't make use of ID3 tags. It's purely folder based. I have my music sorted in folders. Each folder can be an album from one artist or a collection of miscelancelous music. The tags don't matter. The only requirement is that the folder has a unique name. I use a numbered system.

One of the main folders is "246 Classic Rock".

In that folder there is for instance "246.1 Supertramp & Roger Hodgson".

And in that folder you can find "246.1.2 - 1974 Supertramp - Crime Of The Century".

To start that album, you simply put in "246.1.2" and "enter". Then that album starts playing.

You can also enter "246.1" to start playing all albums from Supertramp.

I have a list on paper of all albums and collections, which is just a printout of my folder structure.

By playing a music folder, the playlist is automatically cleared and the whole folder is loaded including subfolders. If you start your folder with "+" in front of it, the playlist won't be cleared. So you can easily put many folders in the playlist.

On each input, the Bluebox app scans your folder structure to find and play the intended folder. So when you add new music, use the official Bluesound app to update the player index and you're done.

## Start playing a radio station ##
The radio stations are also numbered, but starts with a 0. So the Dutch radio 3 is started by entering "03" and "enter". Radio 3 also has some special streams. They are played by entering "03.1" or "03.2". Radio Paradise is played by entering 10, or 101 for the Mellow mix etc.

You can add your own music folders by adding them in radio.cvs, which is a comma seperated file.

# Installation #

## Run it on Windows and a Raspberry Pi ##
The Bluebox app is written in Python 3. I have mine running on three devices: Windows and two Raspberry Pi's running Raspbian (Linux).

## Installation on Windows ##
Put all the app-files in one folder and fill in the needed items in the file app_conf.py.
Install Python3 if needed.
Start the application and see which libraries need to be installed. From what I remember these are: 
```
python3-tk
python-imaging
python-imaging-tk
python3-pil.imagetk
```

## Installation on a Raspberry Pi ##
Install Raspbian, including the graphic environment, on a Raspberry Pi. I use a Raspberry Pi 3b.

Open raspi-config. Set it to boot into the shell invironment with the user already logged in.

Using sudo, create the folder /mnt/mynas

Mount your nas by starting "sudo nano /etc/fstab" and entering
> [ip of your nas]:/volume1/music /mnt/mynas nfs defaults  0  0
Try out the configuration with sudo mount -a

Put the Bluebox application files in the root of the music folder of your nas. Fill in the needed items in the file app_conf.py.

Create the file "bluebox.sh" in the user directory containing:
> python3 /mnt/mynas/app.py

Make the file executable with sudo chmod +x bluebox.sh 

In the user directory make a file ".xsession" and put there:
```
#!/bin/sh
@xset s off
@xset -dpms
@xset s noblank
xset -nocursor
./bluebox.sh
```

Install the needed Python libraries. If I remember correctly, these are:
```
sudo apt-get install python3-tk
sudo apt-get install python-imaging 
sudo apt-get install python-imaging-tk
sudo apt-get install python3-pil.imagetk
```

Start the Bluebox app with entering "./bluebox.sh".

# A physical display, permanently showing the playlist and album art #
I use the ETEPON Raspberry Pi Screen 7 Inch HDMI Monitor. There is one screen layout for all functions. Everything is there and accessable in one glance. 

If you use this display, then with "sudo nano /boot/config.txt" fill in the line:
```
hdmi_cvt 1024 600  60 6 0 0 0
```
