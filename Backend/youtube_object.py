from pytube import YouTube

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

    def getLikes(self):
        return self.likes

    def getDislikes(self):
        return self.dislikes

    def getThumbnailURL(self):
        return self.thumbnail_url