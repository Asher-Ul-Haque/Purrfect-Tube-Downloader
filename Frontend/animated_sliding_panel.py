import customtkinter as ctk

class AnimatedSlidePanel(ctk.CTkFrame):
    def __init__(self, parent, startPos, endPos, orientation='y'):
        super().__init__(master=parent,
                         height=50,
                         corner_radius=10,
                         fg_color='red')

        self.startPos=startPos
        self.endPos=endPos
        self.pos=startPos
        self.atStart=True
        self.orientation=orientation

        if self.orientation=='x':
            self.width = abs(endPos - startPos)
            self.place(relx=self.startPos, y=75, relwidth=self.width)
        else:
            self.height=abs(endPos-startPos)
            self.place(rely=self.startPos, relx=0, relheight=self.height, relwidth=1)

    def animateX(self):
        if self.atStart:
            self.animateLeftwards()
        else:
            self.animateRightwards()

    def animateLeftwards(self):
        if self.pos > self.endPos:
            self.pos -=0.008
            self.place(relx=self.pos, relwidth=self.width, relheight=0.8)
            self.after(5, self.animateLeftwards)
        else:
            self.atStart=False

    def getRelPos(self):
        return self.pos


    def animateRightwards(self):
        if self.pos < self.startPos:
            self.pos +=0.008
            self.place(relx=self.pos, rely=0, relwidth=self.width, relheight=0.8)
            self.after(5, self.animateRightwards)
        else:
            self.atStart=True

    def animateY(self):
        if self.atStart:
            self.animateUpwards()
        else:
            self.animateDownwards()

    def animateUpwards(self):
        if self.pos > self.endPos:
            self.pos -=0.008
            self.place(rely=self.pos, relheight=self.height)
            self.after(5, self.animateUpwards)
        else:
            self.atStart=False

    def animateDownwards(self):
        if self.pos < self.startPos:
            self.pos +=0.008
            self.place(rely=self.pos, relheight=self.height)
            self.after(5, self.animateDownwards)
        else:
            self.atStart=True

    def animate(self):
        if self.orientation=='x':
            self.animateX()
        else:
            self.animateY()