import customtkinter as ctk
import sys
import os
sys.path.append(os.path.abspath('../Frontend'))
from animated_sliding_panel import AnimatedPanel

root=ctk.CTk()
root.minsize(500, 500)
frame=AnimatedPanel(root, 0, 0.5, 'y')
frame.pack()
ctk.CTkButton(root, text='Click me', command=frame.animate).pack()
root.mainloop()
