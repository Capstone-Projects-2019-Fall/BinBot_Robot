from tkinter import *
from PIL import ImageTk, Image

m = Tk()  # main window

canvas = Canvas(m, width=2500, height=2500)
canvas.pack()

img = ImageTk.PhotoImage(Image.open(r"C:\Users\Silva_Surfer\Desktop\newImage.jpg"))

canvas.create_image(20, 20, anchor=NW, image=img)

m.title('BinBot Camera Viewer')

# Test commit
m.mainloop()
