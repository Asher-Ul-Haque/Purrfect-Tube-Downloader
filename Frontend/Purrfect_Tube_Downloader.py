#IMPORTS-
import time

import customtkinter as ctk
import random
import os
from photo_object import Photo
import sys
import threading
import requests
sys.path.append(os.path.abspath('../Backend'))
sys.path.append(os.path.abspath('../Frontend'))
sys.path.append(os.path.abspath('../Downloads'))
from animated_sliding_panel import AnimatedSlidePanel
from youtube_object import YoutubeObject
from youtube_stream import YoutubeStream
from tkinter.filedialog import asksaveasfilename
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
whiteCat=Photo('white_cat.png',100, width=100).getImage()
whiteCatBlink=Photo('white_cat_blink.png', 100, 100).getImage()
blueCat=Photo('blue_cat.png', 100, 100).getImage()
blueCatBlink=Photo('blue_cat_blink.png', 100, 100).getImage()
sun=Photo('sun.png',64,64).getImage()
moon=Photo('moon.png',64,64).getImage()
magnifyingGlass=Photo('magnifying_glass.png',64,64).getImage()
thumbnailBackup=Photo('photo_backup.png', 100, 100).getImage()
cascadeDown=Photo('cascade_button.png',20, 20).getImage()
downloadImage=Photo('download_button.png',64, 64).getImage()
cancelImage=Photo('cancel_button.png',64, 64).getImage()

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
downloadType=ctk.StringVar(value='Choose Download Type')
resolutionChoice=ctk.StringVar(value='Choose Resolution')
openWhenDone = ctk.StringVar(value="off")
animatedTitle=''
cursor=0
url=''
videoStack=[]
streamStack=[]
searchPanelyPos = 0.6
thumbnail=thumbnailBackup
searchPanelIsOpen=False

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
def doNothing(*args):
    pass

def completeDownload(*args):
    time.sleep(1)
    statusLabel.configure(text_color='#00ff00')
    title=videoStack[-1].getTitle()
    if len(title)>55:
        title=title[:52]+'...'
    statusBarText.set(f'Status: Download Complete:- {title}')
    downloadButton.configure(fg_color='#1DB954', text='Download', text_color='white', hover_color='#1DB954', font=subHeadingFont, anchor='e', image=downloadImage, height=20, width=50, compound='left', command=downloadAStream)
    progressBar.place_forget()
    if openWhenDone.get()=='on':
        statusBarText.set('Status: Opening File')
        statusLabel.configure(text_color='#00ff00')
        try:
            os.startfile(streamStack[-1].downloadPath)
        except:
            try:
                import subprocess
                subprocess.call(['open', streamStack[-1].downloadPath])
            except:
                statusBarText.set('Status: Failed to open file')
                statusLabel.configure(text_color='#ff0000')
    streamStack.pop()
    openWhenDone.set('off')

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
def animateSearchPanelUpwards():
    global searchPanelyPos
    if searchPanelyPos > 0.32:
        searchPanelyPos -= 0.008
        searchButton.place(relx=0.9, rely=searchPanelyPos, anchor='center')
        searchBar.place(relx=0.45, rely=searchPanelyPos, anchor='center')
        root.after(5, animateSearchPanelUpwards)
def animateSearchPanelDownwards():
    global searchPanelyPos
    if searchPanelyPos < 0.6:
        searchPanelyPos += 0.008
        searchButton.place(relx=0.9, rely=searchPanelyPos, anchor='center')
        searchBar.place(relx=0.45, rely=searchPanelyPos, anchor='center')
        root.after(5, animateSearchPanelDownwards)

def search(*args, **kwargs):
    global videoStack, url, thumbnail, searchPanelIsOpen
    if searchPanelIsOpen:
        statusBarText.set('Status: Searching')
        statusLabel.configure(text_color='#ffffff')
        urlPanel.animateDownwards()
        animateSearchPanelDownwards()
        statusLabel.tkraise()
    def findVideo(attempts=0):
        global url, searchBar, videoStack, searchPanelIsOpen, thumbnail
        if attempts==0:
            statusBarText.set('Status: Searching')
            statusLabel.configure(text_color='#ffffff')
        else:
            statusBarText.set('Status: Searching. Please wait...')
            statusLabel.configure(text_color='#ffffff')
        if attempts<3:
            url=searchBar.get()
            try:
                yt=YoutubeObject(url)
                time.sleep(0.5)

                # download thumbnail
                thumbnailPath = yt.downloadThumbnail()
                time.sleep(1)
                if thumbnailPath != 'Failed to fetch thumbnail':
                    thumbnail = Photo(thumbnailPath, maintainAspectRatio=True).getImage()
                    thumbnailLabel.configure(image=thumbnail, text='')
                else:
                    thumbnailLabel.configure(image=thumbnailBackup)
                    thumbnailLabel.configure(text_color='#ff0000', text='Failed to fetch thumbnail', font=textFont, compound='bottom')
                    statusBarText.set('Status: Failed to fetch thumbnail')

                # Set the video data
                videoTitleLabel.configure(text=yt.getDisplayableTitle())
                videoDataLabel.configure(text=yt.getDisplayData())

                # Start the animations
                searchPanelIsOpen=True
                animateSearchPanelUpwards()
                urlPanel.animateUpwards()
                statusLabel.tkraise()
                statusBarText.set('Status: Free')
                videoStack.append(yt)
            except:
                time.sleep(1)
                findVideo(attempts+1)
        else:
            statusBarText.set('Status: Failed to find, please check the URL or internet connection')
            statusLabel.configure(text_color='#ff0000')

    findThread=threading.Thread(target=findVideo)
    findThread.start()



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
                       placeholder_text_color='#BB0000')

searchButton.place(relx=0.9, rely=0.6, anchor='center')
searchBar.bind('<Return>', search)
searchBar.place(relx=0.45, rely=0.6, anchor='center')

#--------------------------------------------------

#The dark mode button can be used to toggle dark mode
def modeChange():
    global mode, modeButton
    if mode=='light':
        mode='dark'
        if 'Free' in statusBarText.get() or 'Searching' in statusBarText.get():
            statusLabel.configure(text_color='white')
        modeButton.configure(image=moon, hover_color='#000000')
        closePanelButton.configure(hover_color='#000000')
        searchButton.configure(hover_color='#000000')
        homeButton.configure(hover_color='#000000')
        searchBar.configure(fg_color='#dddddd')
        root.configure(fg_color='#000000')
        try:
            HWND = windll.user32.GetParent(root.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(0x000000)), sizeof(c_int))
        except:
            pass
    else:
        mode='light'
        if 'Free' in statusBarText.get() or 'Searching' in statusBarText.get():
            statusLabel.configure(text_color='black')
        modeButton.configure(image=sun, hover_color='#ffffff')
        closePanelButton.configure(hover_color='#ffffff')
        searchButton.configure(hover_color='#ffffff')
        homeButton.configure(hover_color='#ffffff')
        searchBar.configure(fg_color='#ffffff')
        root.configure(fg_color='#ffffff')
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
    statusBarFreeValues=['Status: Searching', 'Status: Not a valid youtube URL', 'Status: Sorry, No streams found', 'Status: Choose Download Type, please', 'Status: Choose Download Type and Resolution, please', 'Status: No stream found', 'Status: Download cancelled', 'Status: Choose Resolution, please',  'Status: Opening File', 'Status: Failed to open file', 'Status: Download cancelled', 'Status: Failed to find, please check the URL or internet connection', 'Status: Failed to fetch thumbnail']
    if statusBarText.get() in statusBarFreeValues or 'Complete' in statusBarText.get():
        statusBarText.set('Status: Free')
        if mode=='light':
            statusLabel.configure(text_color='black')
        else:
            statusLabel.configure(text_color='white')
    root.after(5000, statusBarClear)

statusLabel.place(relx=0.5, rely=0.975, anchor='center')
statusBarClear()

def goToHomePage():
    global root, url
    root.destroy()
    os.system('python Purrfect_Tube_Downloader.py')

homeButton.configure(command=goToHomePage)

#= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#THE URL RESULT PANEL-
#This panel shows the results of the search of the URL
urlPanel=AnimatedSlidePanel(root, 1, 0.4)
thumbnailLabel=ctk.CTkLabel(master=urlPanel,
                            image=thumbnailBackup,
                            text='',
                            fg_color='transparent',
                            anchor='center',
                            corner_radius=0,
                            width=10,
                            height=10,
                            compound='left')
urlPanel.configure(fg_color='transparent', corner_radius=5, border_color='red', border_width=5)
thumbnailLabel.place(relx=0.165, rely=0.28, anchor='center')

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
videoTitleLabel.place(relx=0.018, rely=0.55)
videoDataLabel.place(relx=0.02, rely=0.7)

#--------------------------------------------------

#Side bar
ctk.CTkLabel(master=urlPanel, text='', width=8, height=296, fg_color='red').place(relx=0.33, rely=0.499, anchor='center')

#--------------------------------------------------

#The download title
ctk.CTkLabel(master=urlPanel, text_color='red', text='Download Options-', font=subHeadingFont, fg_color='transparent', anchor='center', justify='center').place(relx=0.65, rely=0.08, anchor='center')

#--------------------------------------------------

#The close Panel button
def closePanel():
    global url, searchBar
    urlPanel.animateDownwards()
    animateSearchPanelDownwards()
    statusLabel.tkraise()
    searchBar.delete(0, 'end')
    searchBar.insert(0, '')
    searchPanelIsOpen=False

closePanelButton=ctk.CTkButton(master=urlPanel,
                               fg_color='transparent',
                               text='',
                               corner_radius=10,
                               hover_color='#000000',
                               anchor='e',
                               image=cascadeDown,
                               height=5,
                               width=5,
                               compound='left',
                               command=closePanel)
closePanelButton.place(relx=0.95, rely=0.1, anchor='center')

#--------------------------------------------------
#The download configuration Menus
def setDownloadType(choice):
    global downloadType
    downloadType.set(choice)
    if choice=='Audio Only':
        downloadTypeMenu.configure(fg_color='#1DB954', button_color='#199C4B')
        downloadTypeMenu.place(relx=0.65, rely=0.35, anchor='center')
        resolutionMenu.place_forget()
    else:
        downloadTypeMenu.configure(fg_color='red', button_color='#8B0000')
        downloadTypeMenu.place(relx=0.53, rely=0.35, anchor='center')
        resolutionMenu.place(relx=0.83, rely=0.35, anchor='center')
        if choice=='Video Only':
            resolutionList=videoStack[-1].getResolutions(videoOnly=True)
        else:
            resolutionList=videoStack[-1].getResolutions()
        if resolutionList==[]:
            statusBarText.set('Status: Sorry, No streams found')
            statusLabel.configure(text_color='#ff0000')
        resolutionMenu.configure(values=resolutionList)

downloadTypeMenu=ctk.CTkOptionMenu(master=urlPanel,
                                   values=['Video+Audio', 'Video Only', 'Audio Only'],
                                   command=setDownloadType,
                                   variable=downloadType,
                                   text_color='white',
                                   font=textFont,
                                   dropdown_font=textFont,
                                   dropdown_fg_color='#8B0000',
                                   dropdown_hover_color='red',
                                   dropdown_text_color='white',
                                   width=150,
                                   height=30,
                                   corner_radius=5,
                                   fg_color='red',
                                   button_color='#8B0000',
                                   hover=False,
                                   anchor='center')

def setResolutionChoice(choice):
    global resolutionChoice, downloadType
    if downloadType.get()!='Choose Download Type':
        resolutionChoice.set(choice)
    else:
        statusBarText.set('Status: Choose Download Type, please')
        resolutionChoice.set('Choose Resolution')
        statusLabel.configure(text_color='#ff0000')

resolutionMenu=ctk.CTkOptionMenu(master=urlPanel,
                                   values=['Choose Download Type'],
                                   command=setResolutionChoice,
                                   variable=resolutionChoice,
                                   text_color='white',
                                   font=textFont,
                                   dropdown_font=textFont,
                                   dropdown_fg_color='#8B0000',
                                   dropdown_hover_color='red',
                                   dropdown_text_color='white',
                                   width=150,
                                   height=30,
                                   corner_radius=5,
                                   fg_color='red',
                                   button_color='#8B0000',
                                   button_hover_color='#8B0000',
                                   anchor='center')

downloadTypeMenu.place(relx=0.53, rely=0.35, anchor='center')
resolutionMenu.place(relx=0.83, rely=0.35, anchor='center')

#--------------------------------------------------

#The download button
def cancelADownload():
    statusBarText.set('Status: Download cancelled')
    statusLabel.configure(text_color='#ff0000')
    downloadButton.configure(image=downloadImage, text='Download', command=downloadAStream, fg_color='#1DB954', hover_color='#1DB954')
    progressBar.place_forget()
    streamStack.pop().cancelDownload()

def updateProgressBar():
    global progressBar, streamStack
    if len(streamStack)==0:
        return
    if streamStack[-1].getProgressDecimal()<=0.99:
        if streamStack[-1].filesize==0:
            progressBar.set(0)
        else:
            progressBar.set(streamStack[-1].getProgressDecimal())
            title=videoStack[-1].getTitle()
            if len(title)>45:
                title=title[:42]+'...'
            statusBarText.set(f'Status: Downloading {title}  |  {streamStack[-1].getProgressPercentage()} | {streamStack[-1].getDisplayableSize()}/{streamStack[-1].getDisplayableFileSize()}')
        root.after(1, updateProgressBar)

def downloadAStream():
    global streamStack, downloadDirectory, completeDownload
    #Check if resolution and type are chosen
    if downloadType.get()=='Choose Download Type':
        statusBarText.set('Status: Choose Download Type and Resolution, please')
        statusLabel.configure(text_color='#ff0000')
        return
    elif resolutionChoice.get()=='Choose Resolution' and downloadType.get()!='Audio Only':
        statusBarText.set('Status: Choose Resolution, please')
        statusLabel.configure(text_color='#ff0000')
        return
    #Add stream to stram stack
    if downloadType.get()=='Audio Only':
        filename = asksaveasfilename(defaultextension=".mp3", filetypes=[("Audio files", "*.mp3")], initialfile=videoStack[-1].getTitle())
        if filename:
            downloadPath = filename
        else:
            return
        streamStack.append(YoutubeStream(videoStack[-1].streams.filter(only_audio=True).order_by('abr')[-1], downloadPath, None, completeDownload))
    else:
        filename = asksaveasfilename(defaultextension=".mp4", filetypes=[("Video files", "*.mp4")], initialfile=videoStack[-1].getTitle())
        if filename:
            downloadPath = filename
        else:
            return
        chosenStream=YoutubeStream(videoStack[-1].getChosenStream(downloadType.get(), resolutionChoice.get()), downloadPath, updateProgressBar, completeDownload)
        if chosenStream==None:
            statusBarText.set('Status: No stream found')
            statusLabel.configure(text_color='#ff0000')
            return
        streamStack.append(YoutubeStream(videoStack[-1].getChosenStream(downloadType.get(), resolutionChoice.get()), downloadPath, updateProgressBar, completeDownload))
    #Set the download button to cancel
    downloadButton.configure(image=cancelImage, text='Cancel', command=cancelADownload, fg_color='red', hover_color='red')
    progressBar.place(relx=0.65, rely=0.85, anchor='center')
    stream=streamStack[-1]
    # work on the statusLabel when download starts
    statusLabel.tkraise()
    title=videoStack[-1].getTitle()
    if len(title)>55:
        title=title[:52]+'...'
    statusBarText.set(f'Status: Downloading {title},      0%     0.00 MB/{stream.getDisplayableSize()}')
    statusLabel.configure(text_color='#00ff00')
    #begin the download
    downloadThread=threading.Thread(target=stream.downloadVideo)
    downloadThread.start()

downloadButton=ctk.CTkButton(master=urlPanel,
                             fg_color='#1DB954',
                             text='Download',
                             text_color='white',
                             corner_radius=10,
                             hover_color='#1DB954',
                             font=subHeadingFont,
                             anchor='e',
                             image=downloadImage,
                             height=20,
                             width=50,
                             compound='left',
                             command=downloadAStream)
downloadButton.place(relx=0.65, rely=0.6, anchor='center')

#--------------------------------------------------

#Progress bar and label:
progressBar=ctk.CTkProgressBar(master=urlPanel,
                               fg_color='white',
                               width=300,
                               height=10,
                               corner_radius=10,
                               progress_color='#1DB954',
                               orientation='horizontal')
progressBar.set(0)

#--------------------------------------------------

#OpenDecisionSlider
openWhenDoneSwitch = ctk.CTkSwitch(urlPanel, text="", variable=openWhenDone, onvalue="on", offvalue="off", button_color='#1DB954', progress_color='#14906A', button_hover_color='#1DB954')
openWhenDoneLabel = ctk.CTkLabel(urlPanel, text="Open when done", font=displayTextFont, fg_color='transparent', text_color='#1DB954', anchor='center')
openWhenDoneSwitch.place(relx=0.8, rely=0.77, anchor='center')
openWhenDoneLabel.place(relx=0.6, rely=0.77, anchor='center')

#= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#RUN
root.mainloop()