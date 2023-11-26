import customtkinter as ctk

class AnimatedPanel(ctk.CTkFrame):
    def __init__(self, parent, startPos, endPos, orientation):
        super().__init__(master=parent, fg_color='red', corner_radius=10, border_color='red', border_width=10)

        #general atributes
        self.startPos=startPos
        self.endPos=endPos
        self.orientation=orientation

        #animation logic
        self.pos=startPos
        self.atStart=True


        if self.orientation=='x':
            self.width=abs(startPos-endPos)
            self.place(relx=self.startPos, relwidth=self.width, relheight=0.7, rely=0.3)
        elif self.orientation=='y':
            self.height=abs(startPos-endPos)
            self.place(rely=self.startPos, relwidth=1, relheight=self.height, relx=0)

    def animate(self):
        if self.atStart:
            if self.orientation=='x':
                self.animateRightwards()
            else:
                self.animateUpwards()
        else:
            if self.orientation=='x':
                self.animateLeftwards()
            else:
                self.animateDownwards()

    def animateLeftwards(self):
        if self.pos>self.endPos:
            self.pos-=0.01
            self.place(relx=self.pos, relwidth=self.width, relheight=0.7, rely=0.3)
            self.after(8, self.animateLeftwards)
        else:
            self.atStart=False

    def animateRightwards(self):
        if self.pos<self.endPos:
            self.pos+=0.01
            self.place(relx=self.pos, relwidth=self.width, relheight=0.7, rely=0.3)
            self.after(8, self.animateRightwards)
        else:
            self.atStart=True

    def animateUpwards(self):
        if self.pos>self.endPos:
            self.pos-=0.01
            self.place(rely=self.pos, relwidth=1, relheight=self.height, relx=0)
            self.after(8, self.animateUpwards)
        else:
            self.atStart=False

    def animateDownwards(self):
        if self.pos<self.endPos:
            self.pos+=0.01
            self.place(rely=self.pos, relwidth=1, relheight=self.height, relx=0)
            self.after(8, self.animateDownwards)
        else:
            self.atStart=True