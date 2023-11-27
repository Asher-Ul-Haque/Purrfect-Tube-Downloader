#IMPORTS-
import customtkinter as ctk
import random
import os
from photo_object import Photo
import sys
import threading
sys.path.append(os.path.abspath('../Backend'))
sys.path.append(os.path.abspath('../Frontend'))
sys.path.append(os.path.abspath('../Downloads'))
from animated_sliding_panel import AnimatedPanel
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
displayTextFont=('Cooper Black', 10)

#= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#IMAGES-
whiteCat=Photo('white_cat.png').getImage()
whiteCatBlink=Photo('white_cat_blink.png').getImage()
blueCat=Photo('blue_cat.png').getImage()
blueCatBlink=Photo('blue_cat_blink.png').getImage()
sun=Photo('sun.png').getImage(64,64)
moon=Photo('moon.png').getImage(64,64)
magnifyingGlass=Photo('magnifying_glass.png').getImage(64,64)
thumbnailBackup=Photo('photo_backup.png').getImage(150, 150)

#= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#SETTING UP THE ROOT WINDOW-
root=ctk.CTk()
root.geometry('640x512+0+0')
root.minsize(640,512)
root.maxsize(640,512)
root.configure(fg_color='#000000')
root.title('Purrfect Downloads')
root.wm_iconbitmap(os.path.join(Photo.imageDirectory, 'Logo.ico'))

#This works only on windows
try:
    HWND = windll.user32.GetParent(root.winfo_id())
    windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(0x000000)), sizeof(c_int))
except:
    pass

#= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#GLOBAL VARIABLES-
mode='dark'
aspectRatio=5/4
title='Purrfect Tube\nDownloader'
statusBarText=ctk.StringVar(value='Status: Free')
animatedTitle=''
cursor=0
url=''
downloadDirectory = os.path.abspath('../Downloads')
if not os.path.exists(downloadDirectory):
    os.makedirs(downloadDirectory)
downloadStack=[]
searchPanelyPos = 0.6
thumbnail=thumbnailBackup

#= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#THE UTLILITY BUTTONS AND NAME LOGO-
#These buttons are on all the pages

#The cat button can be used to go back to the home page
homeButton=ctk.CTkButton(master=root,
                         fg_color='transparent',
                         text='',
                         corner_radius=10,
                         hover_color='#000000',
                         anchor='e',
                         image=blueCat,
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
def animateSearchPanel():
    atStart=True
    def animateUpwards():
        global searchPanelyPos
        if searchPanelyPos>0.32:
            searchPanelyPos-=0.01
            searchButton.place(relx=0.9, rely=searchPanelyPos, anchor='center')
            searchBar.place(relx=0.45, rely=searchPanelyPos, anchor='center')
            root.after(8, animateUpwards)
        else:
            atStart=False
    def animateDownwards():
        global searchPanelyPos
        if searchPanelyPos < 0.6:
            searchPanelyPos += 0.01
            searchButton.place(relx=0.9, rely=searchPanelyPos, anchor='center')
            searchBar.place(relx=0.45, rely=searchPanelyPos, anchor='center')
            root.after(8, animateDownwards())
        else:
            atStart = True
    if atStart:
        animateUpwards()
    else:
        animateDownwards()

def search(*args, **kwargs):
    def find():
        global url, thumbnail
        url = searchBar.get()
        try:
            statusBarText.set('Status: Searching')
            video = YoutubeObject(url)
            path=video.downloadThumbnail()
            statusLabel.tkraise()
            animateSearchPanel()
            urlPanel.animateUpwards()
            if path!='Failed to fetch thumbnail':
                thumbnail = Photo(path, maintainAspectRatio=True).getImage()
                thumbnailLabel.configure(image=thumbnail)
            else:
                statusBarText.set('Status: Failed to fetch thumbnail')
                statusLabel.configure(text_color='#ff0000')
            statusBarText.set(f'Status: Downloading {video.getTitle()}')
            statusLabel.configure(text_color='#00ff00')
            downloadStack.append(video.getTitle())
            videoTitleLabel.configure(text=video.getDisplayableTitle())
            videoDataLabel.configure(text=video.getDisplayData())
            print(downloadStack)
            videoStream = YoutubeStream(video.best, downloadDirectory).download()
            downloadStack.remove(video.getTitle())
            statusLabel.configure(text_color='#00ff00')
            statusBarText.set('Status: Download Complete')
        except:
            statusBarText.set('Status: Not a valid youtube URL')
            statusLabel.configure(text_color='#ff0000')


    searchThread = threading.Thread(target=find)
    mascotAnimationThread = threading.Thread(target=animateMascot, kwargs={'infinite': False})
    searchThread.start()
    mascotAnimationThread.start()

searchButton=ctk.CTkButton(master=root,
                           fg_color='transparent',
                           text='',
                           corner_radius=20,
                           hover_color='#000000',
                           anchor='e',
                           image=magnifyingGlass,
                           width=8,
                           height=8,
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

searchButton.place(relx=0.9, rely=0.6, anchor='center')
searchBar.bind('<Return>', search)
searchBar.place(relx=0.45, rely=0.6, anchor='center')

#--------------------------------------------------

#The dark mode button can be used to toggle dark mode
def modeChange():
    global mode, modeButton
    if mode=='light':
        mode='dark'
        modeButton.configure(image=moon, hover_color='#000000')
        root.configure(fg_color='#000000')
        homeButton.configure(hover_color='#000000')
        searchBar.configure(fg_color='#dddddd')
        searchButton.configure(hover_color='#000000')
        if 'Free' in statusBarText.get() or 'Searching' in statusBarText.get():
            statusLabel.configure(text_color='white')
        try:
            HWND = windll.user32.GetParent(root.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(0x000000)), sizeof(c_int))
        except:
            pass
    else:
        mode='light'
        modeButton.configure(image=sun, hover_color='#ffffff')
        root.configure(fg_color='#ffffff')
        homeButton.configure(hover_color='#ffffff')
        searchBar.configure(fg_color='#ffffff')
        searchButton.configure(hover_color='#ffffff')
        if 'Free' in statusBarText.get() or 'Searching' in statusBarText.get():
            statusLabel.configure(text_color='black')
        try:
            HWND = windll.user32.GetParent(root.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(0x0000FF)), sizeof(c_int))
        except:
            pass

modeButton=ctk.CTkButton(master=root,
                          fg_color='transparent',
                          text='',
                          corner_radius=10,
                          hover_color='#000000',
                          height=10,
                          width=17,
                          anchor='e',
                          image=moon,
                          compound='left',
                          command=modeChange)
modeButton.place(relx=0.85, rely=0.03)

#--------------------------------------------------

#This is a status bar that is on all the pages. It shows searching etc

statusLabel=ctk.CTkLabel(font=textFont,
                         master=root,
                         fg_color='transparent',
                         text_color='white',
                         textvariable=statusBarText,
                         width=640,
                         anchor='w')

def statusBarClear():
    global statusBarText
    if statusBarText.get()=='Status: Download Complete' or statusBarText.get()=='Status: Failed to fetch thumbnail' or statusBarText.get()=='Status: Not a valid youtube URL':
        statusBarText.set('Status: Free')
        if mode=='light':
            statusLabel.configure(text_color='black')
        else:
            statusLabel.configure(text_color='white')
    root.after(7000, statusBarClear)

statusLabel.place(relx=0.5, rely=0.975, anchor='center')
statusBarClear()

def goToHomePage():
    global root, url
    root.destroy()
    os.system('python run_me.py')

homeButton.configure(command=goToHomePage)

#= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#THE URL RESULT PANEL-
#This panel shows the results of the search of the URL
urlPanel=AnimatedPanel(root, 1, 0.4, 'y')
thumbnailLabel=ctk.CTkLabel(master=urlPanel,
                            image=thumbnailBackup,
                            text='',
                            fg_color='red',
                            anchor='center',
                            corner_radius=0,
                            width=10,
                            height=10,
                            compound='left')
urlPanel.configure(fg_color='#fdfdfd')
thumbnailLabel.place(relx=0.17, rely=0.28, anchor='center')

#--------------------------------------------------

#The title of the video and video data
videoTitleLabel=ctk.CTkLabel(master=urlPanel,
                        font=textFont,
                        fg_color='transparent',
                        text_color='red',
                        anchor='center')
videoDataLabel=ctk.CTkLabel(master=urlPanel,
                        font=textFont,
                        fg_color='transparent',
                        text_color='red',
                        anchor='w',
                        justify='left')
videoTitleLabel.place(relx=0.022, rely=0.55)
videoDataLabel.place(relx=0.02, rely=0.75)

#--------------------------------------------------

#Side bar
ctk.CTkLabel(master=urlPanel, text='', width=10, height=300, fg_color='red', bg_color='white').place(relx=0.33, rely=0.52, anchor='center')


#--------------------------------------------------

#The download title
downloadsLabel=ctk.CTkLabel(master=urlPanel,
                            text_color='red',
                            text='Download Options-',
                            font=subHeadingFont,
                            fg_color='transparent',
                            anchor='center',
                            justify='center')
downloadsLabel.place(relx=0.65, rely=0.08, anchor='center')

#= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#RUN
if __name__=='__main__':
    root.mainloop()