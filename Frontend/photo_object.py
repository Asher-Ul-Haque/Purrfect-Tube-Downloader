import os
from PIL import Image
import customtkinter as ctk
class Photo(object):
    imageDirectory=os.path.abspath('../Assets')
    def __init__(self, imageName, height=64, width=52.8, maintainAspectRatio=False):
        self.imageName=imageName
        self.path=os.path.join(self.imageDirectory, imageName)
        self.imageRaw=Image.open(self.path)
        self.originalWidth, self.originalHeight = self.imageRaw.size
        self.height = int(height)
        self.width = int(width)
        self.originalAspectRatio= self.width / self.height
        self.image=ctk.CTkImage(self.imageRaw, size=(self.height, self.width))

        self.maintainAspectRatio=maintainAspectRatio
    def getImagePath(self):
        return self.path
    def getImageName(self):
        return self.imageName
    def getHeight(self):
        return self.height
    def getWidth(self):
        return self.width
    def getImageRaw(self):
        return self.imageRaw
    def getImage(self):
        if self.maintainAspectRatio:
            self.width=150
            self.height=int(self.width/self.originalAspectRatio)
        return ctk.CTkImage(self.imageRaw, size=(self.height, self.width))