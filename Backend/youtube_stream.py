import os
import threading
from pytube import request
import time
class YoutubeStream:
    def __init__(self, stream, downloadPath, progressCallback, completionCallback):
        self.cancelled = False
        self.stream = stream
        self.title = stream.title
        self.codecs = stream.codecs
        self.progressCallback = progressCallback
        self.completionCallback = completionCallback
        self.currentSize = 0
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
        self.downloadPath = downloadPath

    def downloadVideo(self):
        self.cancelled = False
        with open(self.downloadPath, 'wb') as f:
            is_cancelled = False
            stream = request.stream(self.stream.url)
            while True:
                if self.cancelled:
                    print('Download cancelled')
                    break
                chunk = next(stream, None)
                if chunk:
                    if self.progressCallback==None:
                        pass
                    else:
                        self.progressCallback()
                    self.currentSize += len(chunk)
                    f.write(chunk)
                else:
                    print('Download completed')
                    if self.completionCallback==None:
                        pass
                    else:
                        self.completionCallback()
                    break

    def cancelDownload(self):
        self.cancelled = True
        time.sleep(1)
        os.remove(self.downloadPath)
        print('File deleted')

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

    def getDirectoryPath(self):
        return self.directoryPath

    def getDownloadPath(self):
        return self.downloadPath

    def getDisplayableSize(self):
        sizeBytes = self.currentSize
        units = ['B', 'KB', 'MB', 'GB']
        unitsIndex = 0
        while sizeBytes > 1024 and unitsIndex < len(units) - 1:
            sizeBytes /= 1024.0
            unitsIndex += 1
        sizeFormatted = "{:.1f} {}".format(sizeBytes, units[unitsIndex])
        return sizeFormatted

    def getDisplayableFileSize(self):
        sizeBytes = self.filesize
        units = ['B', 'KB', 'MB', 'GB']
        unitsIndex = 0
        while sizeBytes > 1024 and unitsIndex < len(units) - 1:
            sizeBytes /= 1024.0
            unitsIndex += 1
        sizeFormatted = "{:.1f} {}".format(sizeBytes, units[unitsIndex])
        return sizeFormatted

    def getProgressPercentage(self):
        return f'{self.currentSize/self.filesize*100:.1f}%'

    def getProgressDecimal(self):
        return float(f'{self.currentSize/self.filesize:.1f}')



