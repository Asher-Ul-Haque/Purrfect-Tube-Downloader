#IMPORTS-
import customtkinter as ctk
import random
import os
from Photo import Photo
import sys
import threading
sys.path.append(os.path.abspath('../Backend'))
sys.path.append(os.path.abspath('../Downloads'))
from youtube_object import YoutubeObject
from youtube_stream import YoutubeStream
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

#= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#FONTS-
headingFont=('Cooper Black', 50, 'bold')
subHeadingFont=('Cooper Black', 16)
textFont=('Cooper Black', 12)

#= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#IMAGES-
whiteCat=Photo('white_cat.png').getImage()
whiteCatBlink=Photo('white_cat_blink.png').getImage()
blueCat=Photo('blue_cat.png').getImage()
blueCatBlink=Photo('blue_cat_blink.png').getImage()
sun=Photo('sun.png').getImage(64,64)
moon=Photo('moon.png').getImage(64,64)
magnifyingGlass=Photo('magnifying_glass.png').getImage(64,64)
print(magnifyingGlass)

#= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#SETTING UP THE ROOT WINDOW-
root=ctk.CTk()
root.geometry('640x512+0+0')
root.minsize(640,512)
root.maxsize(640,512)
root.configure(fg_color='white')
root.title('Purrfect Downloads')
root.wm_iconbitmap(os.path.join(Photo.imageDirectory, 'Logo.ico'))

#This works only on windows
try:
    HWND = windll.user32.GetParent(root.winfo_id())
    windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(0x0000FF)), sizeof(c_int))
except:
    pass

#= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#GLOBAL VARIABLES-
mode='light'
aspectRatio=5/4
title='Purrfect Tube\nDownloader'
searchBarText='...'
animatedSearchBarText=''
animatedTitle=''
cursor=0
url=''
downloadDirectory = os.path.abspath('../Downloads')
searchButtony=0.6

#= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#THE UTLILITY BUTTONS AND NAME LOGO-
#These buttons are on all the pages

#The cat button can be used to go back to the home page
homeButton=ctk.CTkButton(master=root,
                         fg_color='transparent',
                         text='',
                         corner_radius=10,
                         hover_color='#ffffff',
                         anchor='e',
                         image=whiteCat,
                         width=5,
                         height=5,
                         compound='left')

def animateMascot(infinite=True):
    global mode
    if infinite:
        if mode=='light':
            homeButton.configure(image=whiteCat)
            root.after(random.randint(50, 1000), animateMascot)
            if random.randint(0, 10)//2==0:
                homeButton.configure(image=whiteCatBlink)
        else:
            homeButton.configure(image=blueCat)
            root.after(random.randint(50, 1000), animateMascot)
            if random.randint(0, 10)//2==0:
                homeButton.configure(image=blueCatBlink)
    else:
        for i in range(3):
            if mode=='light':
                homeButton.configure(image=whiteCat)
                if random.randint(0, 10)//2==0:
                    homeButton.configure(image=whiteCatBlink)
            else:
                homeButton.configure(image=blueCat)
                if random.randint(0, 10)//2==0:
                    homeButton.configure(image=blueCatBlink)
animateMascot()
homeButton.place(relx=0.03, rely=0.0)

#--------------------------------------------------

#The name logo-
titleLabel=ctk.CTkLabel(text='SAMPLE',
                        font=headingFont,
                        master=root,
                        text_color='red')
titleLabel.pack(side='top', pady=20)
def doNothing():
    pass

def animateHeading():
    global animatedTitle, title, cursor
    if animatedTitle!=title:
        titleLabel.configure(text=animatedTitle)
        animatedTitle+=title[cursor]
        root.after(100, animateHeading)
        cursor+=1
    else:
        root.after(100, doNothing)
        titleLabel.configure(text=title)

animateHeading()

#--------------------------------------------------
#The search bar and button-

def search(*args, **kwargs):
    try:
        def find():
            global url
            url = searchBar.get()
            video = YoutubeObject(url)
            videoStream = YoutubeStream(video.best, downloadDirectory).download()
            print('Download Completed')
        searchThread=threading.Thread(target=find)
        mascotAnimationThread=threading.Thread(target=animateMascot, kwargs={'infinite':False})
        searchThread.start()
        mascotAnimationThread.start()

    except:
        print('Not a valid youtube URL')

searchButton=ctk.CTkButton(master=root,
                           fg_color='transparent',
                           text='',
                           corner_radius=20,
                           hover_color='#ffffff',
                           anchor='e',
                           image=magnifyingGlass,
                           width=1,
                           height=1,
                           compound='left',
                           command=search)

searchBar=ctk.CTkEntry(master=root,
                       fg_color='white',
                       bg_color='transparent',
                       text_color='#EE0000',
                       font=textFont,
                       corner_radius=5,
                       width=500,
                       height=50,
                       placeholder_text='Enter the URL of the video',
                       placeholder_text_color='#CD0000')

searchButton.place(relx=0.1, rely=0.6, anchor='center')
searchBar.bind('<Return>', search)
searchBar.place(relx=0.55, rely=0.6, anchor='center')

#--------------------------------------------------

#The dark mode button can be used to toggle dark mode
def modeChange():
    global mode
    if mode=='light':
        mode='dark'
        modeButton.configure(image=moon)
        root.configure(fg_color='#000000')
        homeButton.configure(hover_color='#000000')
        searchBar.configure(fg_color='#dddddd')
        searchButton.configure(hover_color='#000000')
        try:
            HWND = windll.user32.GetParent(root.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(0x000000)), sizeof(c_int))
        except:
            pass
    else:
        mode='light'
        modeButton.configure(image=sun)
        root.configure(fg_color='#ffffff')
        homeButton.configure(hover_color='#ffffff')
        searchBar.configure(fg_color='#ffffff')
        searchButton.configure(hover_color='#ffffff')
        try:
            HWND = windll.user32.GetParent(root.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(0x0000FF)), sizeof(c_int))
        except:
            pass

modeButton=ctk.CTkButton(master=root,
                          fg_color='transparent',
                          text='',
                          corner_radius=10,
                          hover_color='#dddddd',
                          height=10,
                          width=17,
                          anchor='e',
                          image=sun,
                          compound='left',
                          command=modeChange)
modeButton.place(relx=0.85, rely=0.03)

#= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#RUN
if __name__=='__main__':
    root.mainloop()