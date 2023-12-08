import os
class YoutubeStream:
    def __init__(self, stream, downloadPath):
        self.stream = stream
        self.title = stream.title
        self.codecs = stream.codecs
        try:
            self.resolution = stream.resolution
            self.fps = stream.fps
        except:
            pass
        self.filesize = stream.filesize
        self.url = stream.url
        self.itag = stream.itag
        self.mime_type = stream.mime_type
        self.abr = stream.abr
        self.type = stream.type
        self.downloadPath=downloadPath

    def download(self):
        self.stream.download(output_path=self.downloadPath, skip_existing=False, max_retries=3)

    def getStream(self):
        return self.stream

    def getTitle(self):
        return self.title

    def getCodecs(self):
        return self.codecs

    def getResolution(self):
        return self.resolution

    def getFps(self):
        return self.fps

    def getFilesize(self):
        return self.filesize

    def getUrl(self):
        return self.url

    def getItag(self):
        return self.itag

    def getMime_type(self):
        return self.mime_type

    def getAbr(self):
        return self.abr

    def getType(self):
        return self.type

    def getFilesize(self):
        return self.filesize

    def getDownloadPath(self):
        return self.downloadPath

    def getDisplayableSize(self):
        sizeBytes = os.path.getsize(self.downloadPath)
        units = ['B', 'KB', 'MB', 'GB']
        unitsIndex = 0
        while sizeBytes > 1024 and unitsIndex < len(units) - 1:
            sizeBytes /= 1024.0
            unitsIndex += 1
        sizeFormatted = "{:.1f} {}".format(sizeBytes, units[unitsIndex])
        return sizeFormatted

    def getProgress(self):
        sizeBytes = os.path.getsize(self.downloadPath)
        return f'{sizeBytes/self.filesize*100:.1f}%'



