from pytube import YouTube
import requests
import os

class YoutubeObject:
    def __init__(self, url):
        self.url = url
        self.yt = YouTube(url)
        self.streams = self.yt.streams
        self.title = self.yt.title
        self.author = self.yt.author
        self.length = self.yt.length
        self.rating = self.yt.rating
        self.views = self.yt.views
        self.thumbnail_url = self.yt.thumbnail_url
        self.best = self.yt.streams.get_highest_resolution()

    def getURL(self):
        return self.url

    def getYoutubeObject(self):
        return self.yt

    def getStreams(self):
        return self.streams

    def getTitle(self):
        return self.title

    def getAuthor(self):
        return self.author

    def getLength(self):
        return self.length

    def getRating(self):
        return self.rating

    def getViews(self):
        return self.views

    def getThumbnailURL(self):
        return self.thumbnail_url

    def downloadThumbnail(self):
        response = requests.get(self.thumbnail_url)
        thumbnailDirectory = os.path.abspath('../Assets/Thumbnails')
        if response.status_code == 200:
            path = os.path.join(thumbnailDirectory, self.title + ".png")
            with open(path, "wb") as thumbnail:
                thumbnail.write(response.content)
            return path
        else:
            return 'Failed to fetch thumbnail'

    def getDisplayableTitle(self):
        words=self.title.split(' ')
        displayableTitleline1=''
        displayableTitleline2=''
        displayableTitleline3=''
        for word in words:
            if len(displayableTitleline1)+len(word)<30:
                displayableTitleline1 += word+' '
            elif len(displayableTitleline2)+len(word)<30:
                displayableTitleline2 += word+' '
            elif len(displayableTitleline3)+len(word)<30:
                displayableTitleline3 += word+' '
        return displayableTitleline1 + '\n'+ displayableTitleline2 + '\n'+ displayableTitleline3
    def getDisplayData(self):
        minutes=0
        hours=0
        seconds=self.length
        thousands=0
        millions=0
        ones=0
        data=''
        data+='by: '+self.author[:25]
        data+='\n'
        data+='time: '
        if self.length<60:
            data+='0:'+str(self.length)
        elif 60<self.length<3600:
            minutes=self.length//60
            seconds=self.length%60
            data+=str(minutes)+':'+str(seconds)
        else:
            hours=self.length//3600
            minutes=(self.length%3600)//60
            seconds=(self.length%3600)%60
            data+=str(hours)+':'+str(minutes)+':'+str(seconds)
        data+='\n'
        if self.views<1000:
            data+='views: '+str(self.views)
        elif self.views<1000000:
            thousands=self.views//1000
            ones=(self.views%1000)
            data+=str(thousands)+'.'+str(ones)[:2]+'K views'
        else:
            millions=self.views//1000000
            thousands=(self.views%1000000)
            data+=str(millions)+'.'+str(thousands)[:2]+'M views'
        return data

