import customtkinter as ctk

class CompositeButton():
    def __init__(self, stream, root, type, photo):
        self.stream=stream
        self.progress=ctk.StringVar(value='0%')
        self.state=ctk.StringVar(value='Download')
        self.type=type
        self.photo=photo
        if self.type=='video':
            self.title=self.stream.getResolution()
        else:
            self.title='Audio'

        self.titleLabel=ctk.CTkLabel(master=root,
                                     text=self.title,
                                     corner_radius=0,
                                     width=55,
                                     height=10,
                                     text_color='white')
        if self.type=='video':
            self.titleLabel.configure(fg_color='red')
        else:
            self.titleLabel.configure(fg_color='#1DB954')

        self.stateLabel=ctk.CTkButton(master=root,
                                      text='Download',
                                      corner_radius=10,
                                      width=75,
                                      height=10,
                                      fg_color='red')

        self.downloadLabel=ctk.CTkLabel(master=root,
                                        text='',
                                        corner_radius=0,
                                        width=20,
                                        height=10,
                                        image=self.photo,
                                        compound='center',
                                        text_color='white')

        def ShowProgress(self):
            self.stateLabel.configure(text='Cancel')
            if self.title!='Completed':
                self.progress.set(self.stream.getProgress())
                root.after(100, ShowProgress)

    def setPlacement(self, relx=0, rely=0):
        self.stateLabel.place(relx=relx, rely=rely)
        self.titleLabel.place(relx=relx+20, rely=rely+10)
        self.downloadLabel.place(relx=relx, rely=rely+10)