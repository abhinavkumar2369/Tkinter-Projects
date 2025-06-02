from tkinter import *
from time import strftime
from PIL import Image, ImageTk

# Creating Instance of the Window
window = Tk()


# --------------------------------------------------------------


# Ensure High DPI awareness on Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


# -----------------  Title & Dimensions  -------------------------


window.title("Digital Clock")
window.geometry("500x300")
window.resizable(0, 0)
window.configure(bg="white")


# ------------------------- Functions ----------------------------


def display_time():
    current_time = strftime('%H:%M:%S %p')
    label.config(text=current_time)
    label.after(1000, display_time)  # Refresh every second



# Load the image
image = Image.open("./logo.png")
image = image.resize((80, 80))
image = ImageTk.PhotoImage(image)


# Logo 
window.iconphoto(False, image)


# ------------------------- Label ----------------------------


Heading = Label(window, text="Digital  Clock", font=('calibri', 30, 'bold'), foreground='black', bg='white', compound=LEFT, image=image, padx=20, pady=10)
Heading.pack(anchor='center', pady=(20,30) )


label = Label(window, font=('calibri', 40, 'bold'), foreground='black', padx=30, pady=20)
label.pack(anchor='center')


# Function Call
display_time()

# Tkinter Main Loop
window.mainloop()