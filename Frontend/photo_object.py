import os
from PIL import Image
import customtkinter as ctk
class Photo(object):
    imageDirectory=os.path.abspath('../Assets')
    def __init__(self, imageName, height=64, width=52.8):
        self.imageName=imageName
        self.path=os.path.join(self.imageDirectory, imageName)
        self.imageRaw=Image.open(self.path)
        self.image=ctk.CTkImage(self.imageRaw, size=(height, width))
        self.height=height
        self.width=width
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
    def getImage(self, height=100, width=100):
        return ctk.CTkImage(self.imageRaw, size=(height, width))