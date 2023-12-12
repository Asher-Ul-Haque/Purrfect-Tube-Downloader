import customtkinter as ctk

class CompoundVideoFrame(ctk.CTkFrame):
    def __init__(self, parent, thumbnail, videoTitle, videoData):
        super().__init__(master=parent,
                         width=500,
                         height=50,
                         fg_color='transparent')

        self.thumbnail=thumbnail
        self.videoTitle=videoTitle
        self.videoData=videoData

        self.thumbnail.place(relx=0.05, rely=0.1, relheight=0.8, relwidth=0.2)
        self.videoTitle.place(relx=0.3, rely=0.1, relheight=0.8, relwidth=0.6)