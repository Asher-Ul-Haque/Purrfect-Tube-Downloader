from pytube import YouTube
import requests
import os

class YoutubeObject:
    def __init__(self, url):
        self.url = url
        self.yt = YouTube(self.url)
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
        displayableTitle=''
        # line1=''
        # line2=''
        # line3=''
        # for wordIndex in words:
        #     if len(line1)+len(words[wordIndex])<30:
        #         line1+=words[wordIndex]+' '
        #         words.pop(wordIndex)
        #     elif len(line2)+len(words[wordIndex])<30:
        #         line2+=words[wordIndex]+' '
        #         words.pop(wordIndex)
        #     elif len(line3)+len(words[wordIndex])<30:
        #         line3+=words[wordIndex]+' '
        #         words.pop(wordIndex)
        # displayableTitle+=line1+'\n'+line2+'\n'+line3
        # return displayableTitle

        letters=0
        for word in words:
            if letters+len(word)>30:
                displayableTitle+='\n'
                letters=0
            displayableTitle += word+' '
            letters+=len(word)+1
        if len(displayableTitle)>90:
            displayableTitle=displayableTitle[:87]+'...'
        return displayableTitle
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

