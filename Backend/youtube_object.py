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

    def _getUniqueStreams(self, unsortedList):
        uniqueStreams = []
        for stream in unsortedList:
            if str(stream.type) == 'audio':
                if not any(s.abr == stream.abr for s in uniqueStreams):
                    uniqueStreams.append(stream)
            else:
                if not any(s.resolution == stream.resolution and s.fps == stream.fps for s in uniqueStreams):
                    uniqueStreams.append(stream)
        return uniqueStreams

    def getChosenStream(self, type='Video+Audio', resolution='720p: (0.0 MB)'):
        resolution=resolution.split(':')[0]
        if type=='Video+Audio':
            for stream in self.getVideoAndAudioStreams():
                if stream.resolution==resolution:
                    return stream
        else:
            for stream in self.getVideoOnlyStreams():
                if stream.resolution == resolution:
                    return stream

    def downloadThumbnail(self):
        dirMain = os.getcwd()
        os.chdir('../Assets')
        if not os.path.exists('Thumbnails'):
            os.mkdir('Thumbnails')
        os.chdir('Thumbnails')
        try:
            response = requests.get(self.thumbnail_url)
            if response.status_code == 200:
                path = os.path.join(os.getcwd(), self.title + ".png")
                with open(path, "wb") as thumbnail:
                    thumbnail.write(response.content)
                return path
        except:
            return 'Failed to fetch thumbnail'

    def getDisplayableTitle(self):
        words=self.title.split(' ')
        displayableTitle=''
        letters=0
        for word in words:
            if letters+len(word)>25:
                displayableTitle+='\n'
                letters=0
            displayableTitle += word+' '
            letters+=len(word)+1
        if len(displayableTitle)>75:
            displayableTitle=displayableTitle[:72]+'...'
        return displayableTitle

    def getDisplayableAuthor(self):
        words=self.author.split(' ')
        displayableAuthor=''
        letters=0
        for word in words:
            if letters+len(word)>25:
                displayableAuthor+='\n'
                letters=0
            displayableAuthor += word+' '
            letters+=len(word)+1
        if len(displayableAuthor)>75:
            displayableTitle=displayableAuthor[:72]+'...'
        return 'by: '+displayableAuthor

    def getAudioOnlyStreams(self):
        return self._getUniqueStreams(self.streams.filter(only_audio=True))
    def getVideoOnlyStreams(self):
        return self._getUniqueStreams(self.streams.filter(only_video=True, file_extension='mp4', progressive=True))

    def getVideoAndAudioStreams(self):
        return self._getUniqueStreams(self.streams.filter(only_video=False, only_audio=False, file_extension='mp4', progressive=True))

    def getResolutions(self, videoOnly=False):
        global video
        resolutionList = []
        if videoOnly:
            for stream in self._getUniqueStreams(self.streams.filter(only_video=True, file_extension='mp4', progressive=True).order_by('resolution')):
                if stream.resolution in ['144p', '240p', '360p', '480p', '720p', '1080p', '1440p',
                                         '2160p'] and stream.resolution not in resolutionList:
                    resolutionList.append(f'{stream.resolution}: ({self.getDisplayableFilesize(stream.filesize)})')
        else:
            for stream in self._getUniqueStreams(
                    self.streams.filter(only_video=False, only_audio=False, file_extension='mp4', progressive=True).order_by('resolution')):
                if stream.resolution in ['144p', '240p', '360p', '480p', '720p', '1080p', '1440p',
                                         '2160p'] and stream.resolution not in resolutionList:
                    resolutionList.append(f'{stream.resolution}: ({self.getDisplayableFilesize(stream.filesize)})')
        return resolutionList

    def getDisplayData(self):
        minutes=0
        hours=0
        seconds=self.length
        thousands=0
        millions=0
        ones=0
        data=''
        data += self.getDisplayableAuthor()
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
        data+='views: '
        if self.views<1000:
            data+='views: '+str(self.views)
        elif self.views<1000000:
            thousands=self.views//1000
            ones=(self.views%1000)
            data+=str(thousands)+'.'+str(ones)[:2]+'K'
        else:
            millions=self.views//1000000
            thousands=(self.views%1000000)
            data+=str(millions)+'.'+str(thousands)[:2]+'M'
        return data

    def getDisplayableFilesize(self, size):
        units = ['B', 'KB', 'MB', 'GB']
        unitsIndex = 0
        while size > 1024 and unitsIndex < len(units) - 1:
            size /= 1024.0
            unitsIndex += 1
        sizeFormatted = f"{size:.1f} {units[unitsIndex]}"
        return sizeFormatted



