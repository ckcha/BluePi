import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk, ImageFilter, ImageFont, ImageDraw
import platform
import time
import os, psutil, gc
import tracemalloc
from app_logic import *
from socket import timeout
import errno
from socket import error as socket_error
import os

GUI_UPDATE_DELAY = 600

class Main(tk.Tk):

    def __init__(self, parent=None):
        tk.Tk.__init__(self, parent)
        self.configure(background="black")
        self.parent = parent
        self.geometry('720x720')
        self.title("BluPi")
        self.wm_attributes('-fullscreen', 'True')
        self.config(cursor="none")

        self.status = Status()
        self.control = Control(self.status)

        self.bind("<Escape>", exit)

        self.setframes()
        
    def setframes(self):

        self.frame1 = frame1(self, self.status, self.control)

        self.frame1.grid(row=2, column=0, sticky=tk.NW+tk.SE, padx=0, pady=0) 

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        
        self.grid_columnconfigure(0, weight=1)
        

class frame1(tk.Frame): # Image
    def __init__(self, parent, status, control):
        tk.Frame.__init__(self, parent, bg="black", highlightbackground="black",  \
            highlightcolor="black", highlightthickness=0, bd= 0)
        self.img_label = tk.Label(self, bg="black")
        self.img_label.pack(fill = "both", expand = True)
        self.path = os.path.dirname(os.path.abspath(__file__))
        print(self.path)
        self.currentimage_link = ""
        self.currentsong = ""
        self.currentradiosong = ""
        self.currentstate = ""
        self.currentapp = ""
        self.currentimg = Image.new('RGBA', size = (720, 720), color = (128, 128, 128, 255))
        self.parent = frame1
        self.status = status
        self.control = control
        self.albumart = Albumart(self.status)
        self.currentvol = self.status.check_volume()
        self.volchange = 0
        self.seconds = time.time()
        tracemalloc.start(25)
        self.threading_image_update()

    def threading_image_update(self):
        threadObj = threading.Thread(target=self.display_new_image_if_needed)
        threadObj.start()
        
    def display_new_image_if_needed(self):
        while True:

            self.screen_update()
            self.volume_update()
                
            time.sleep(0.5)

    def screen_update(self):
        try:
            song = self.status.check_songname()
        except socket_error as serr:
            song = self.currentsong
            print("socket error: screen update")
        if song != self.currentsong:
            albumart = self.albumart.return_image_link()
            if albumart != False:
                artist = self.status.check_artist()
                self.currentimage_link = albumart
                self.currentsong = song
                songTitle = artist + " ● " + song
                print(songTitle)
                    
                if song == "TV":
                    img = Image.open(os.path.join(self.path, "APP_images/tv.png"))
                else:
                    if song == "Turntable":
                        img = Image.open(os.path.join(self.path, "APP_images/turntable.png"))
                    else:
                        if albumart.startswith("http"):
                            try:
                                imgOG = Image.open(urllib.request.urlopen(albumart, timeout=10)).convert("RGBA")                                
                            except (HTTPError, URLError, IOError) as error:
                                print("HTTPError, URLError: "+albumart)
                                img = Image.open(os.path.join(self.path, "APP_images/nikkatato.jpg"))
                            except timeout:
                                print("socket timed out: "+albumart)
                                img = Image.open(os.path.join(self.path, "APP_images/nikkatato.jpg"))
                            except socket_error as serr:
                                print("socket error: "+albumart)
                                img = Image.open(os.path.join(self.path, "APP_images/nikkatato.jpg"))
                            else:
                                #print("URL success: "+albumart)
                                quality = self.status.check_quality()
                                print("Quality: "+quality)
                                imgL = imgOG.resize((720,720), Image.ANTIALIAS)
                                img = imgL.filter(ImageFilter.GaussianBlur(30))
                                #imgS = Image.open(urllib.request.urlopen(albumart)).convert("RGBA")
                                imgS = imgOG.resize((600,600), Image.ANTIALIAS)
                                img.paste(imgS, (60, 60), imgS)
                                draw = ImageDraw.Draw(img)
                                # font = ImageFont.truetype(<font-file>, <font-size>)
                                font = ImageFont.truetype(os.path.join(self.path, "fonts/arialuni.ttf"), 32)
                                # draw.text((x, y),"Sample Text",(r,g,b))
                                W, H = (720,720)
                                w, h = draw.textsize(songTitle, font=font)
                                pixelRGB = img.getpixel((W/2,H-40))
                                #print(pixelRGB)
                                R,G,B,A = pixelRGB
                                LuminanceA = (0.2126*R) + (0.7152*G) + (0.0722*B)
                                if LuminanceA <= 127:
                                    draw.text(((W-(w))/2,H-55),songTitle,(255,255,255),font=font)
                                else:
                                    draw.text(((W-(w))/2,H-55),songTitle,(48,48,48),font=font)
                                imgL.close()
                                imgS.close()
                                imgOG.close()
                        else:
                            img = Image.open(albumart)
                basewidth = 720
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img_resized = img.resize((basewidth,hsize), Image.ANTIALIAS)
                self.currentimg = img_resized.convert('RGBA')
                render = ImageTk.PhotoImage(img_resized)
                self.img_label.configure(image=render)
                self.img_label.image = render
                img.close()
                img_resized.close()

            else: 
                print("Cannot retrieve album art")
            del albumart
        del song
        

    def volume_update(self):
        try:
            volume = self.status.check_volume()
        except socket_error as serr:
            volume = self.currentvol
            print("socket error: volume update")
                  
        if volume != self.currentvol:
            self.currentvol = self.status.check_volume()
            img = self.currentimg.convert('RGBA')

            foreground = Image.new('RGBA', (720, 720), (0, 0, 0, 0))
            draw = ImageDraw.Draw(foreground)

            # Draw the circle:
            p_x, p_y = 360, 360
            draw.ellipse((p_x - 300, p_y - 300, p_x + 300, p_y + 300), fill=(64, 64, 64, 172))
            font = ImageFont.truetype(os.path.join(self.path, "fonts/JosefinSans-Medium.ttf"), 384)
            W, H = (720,720)
            w, h = draw.textsize(self.currentvol, font=font)
            draw.text(((W-w)/2,(H-h)/2),self.currentvol,(255,255,255),font=font)
                            
            image_new = Image.composite(foreground, img, foreground)
            render = ImageTk.PhotoImage(image_new)
            self.img_label.configure(image=render)
            self.img_label.image = render
            self.volchange = 1
            self.seconds = time.time()
            process = psutil.Process(os.getpid())
            img.close()
            image_new.close()
            foreground.close()
            process = psutil.Process(os.getpid())

        else:
            if time.time() > (self.seconds+6) \
               and self.volchange == 1:
                img = self.currentimg.convert('RGBA')
                render = ImageTk.PhotoImage(img)
                self.img_label.configure(image=render)
                self.img_label.image = render
                self.volchange = 0
                process = psutil.Process(os.getpid())
                print(process.memory_info().rss)  # in bytes
                img.close()

        del volume

if __name__=="__main__":
    app = Main(None)
    app.mainloop()
