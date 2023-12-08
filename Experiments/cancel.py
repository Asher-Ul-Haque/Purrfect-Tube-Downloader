import threading
from pytube import YouTube, request
import os
import time

is_cancelled = False

def download_video(url):
    global is_cancelled

    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    filesize = stream.filesize

    with open('sample.mp4', 'wb') as f:
        is_cancelled = False
        stream = request.stream(stream.url)
        downloaded = 0

        while True:
            if is_cancelled:
                print('Download cancelled')
                break

            chunk = next(stream, None)
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                print(f'Downloaded {downloaded} / {filesize}')
            else:
                print('Download completed')
                break

def start_download(url):
    threading.Thread(target=download_video, args=(url,), daemon=True).start()

def cancel_download():
    global is_cancelled
    is_cancelled = True
    time.sleep(1)
    os.remove('sample.mp4')
    print('File deleted')


# Start the download
start_download('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

# Cancel the download
input('Press enter to cancel the download')
cancel_download()

