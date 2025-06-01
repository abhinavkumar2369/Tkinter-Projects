# Importing Tkinter Module
from tkinter import *
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

window.title("Calculator")
window.minsize(width=450, height=600)
window.maxsize(width=450, height=600)
window.resizable(0, 0)
window.configure(bg="white")


# Load the image
image = Image.open("./logo.png")
image = image.resize((50, 50))
image = ImageTk.PhotoImage(image)

window.iconphoto(False,image)



# ----------------------  Heading Label  ---------------------------


# label
heading_label = Label(window, text="CALCULATOR", font=("Arial", 24), fg="#383b47", pady=20, bg="white", compound=LEFT, image=image)
heading_label.pack(fill="x", padx=10, pady=10)


# ----------------------  Output Screen  ---------------------------

output_screen_entry = Label(window, font=("Arial", 18), fg="black", bg="light gray", relief="flat", bd="3" ,anchor="e")
output_screen_entry.pack(fill="x",padx=30)

output = ""
output_screen = Label(window,text=output, font=("Arial", 18), fg="black", bg="light gray", relief="flat", bd="3", anchor="e")
output_screen.pack(fill="x",padx=30)


# ------------------------- Functions ----------------------------

def add_to_output(value):
    global output
    output = output + str(value)
    output_screen_entry.config(text=output)
    return output

def clear_output():
    global output
    output = ""
    output_screen_entry.config(text=output)
    return output

def calculate_output():
    global output
    try:
        output = str(eval(output))
    except:
        output = "!! Error"
    output_screen.config(text=output)
    return output

# ---------------------------- Buttons  -----------------------------

# Buttons Frame
frame = Frame(window,bg="white",pady=30)
frame.pack(fill="x",padx=30)

# 1
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text=1,font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: add_to_output(1))
button.pack()
button_label.grid(row=0,column=0,padx=15,pady=15)

# 2
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text=2,font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: add_to_output(2))
button.pack()
button_label.grid(row=0,column=1,padx=15,pady=15)

# 3
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text=3,font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: add_to_output(3))
button.pack()
button_label.grid(row=0,column=2,padx=15,pady=15)

# + 
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text="+",font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: add_to_output("+"))
button.pack()
button_label.grid(row=0,column=3,padx=15,pady=15)

# 4
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text=4,font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: add_to_output(4))
button.pack()
button_label.grid(row=1,column=0,padx=15,pady=15)

# 5
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text=5,font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: add_to_output(5))
button.pack()
button_label.grid(row=1,column=1,padx=15,pady=15)

# 6
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text=6,font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: add_to_output(6))
button.pack()
button_label.grid(row=1,column=2,padx=15,pady=15)

# -
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text="-",font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: add_to_output("-"))
button.pack()
button_label.grid(row=1,column=3,padx=15,pady=15)

# 7
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text=7,font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: add_to_output(7))
button.pack()
button_label.grid(row=2,column=0,padx=15,pady=15)

# 8
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text=8,font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: add_to_output(8))
button.pack()
button_label.grid(row=2,column=1,padx=15,pady=15)

# 9
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text=9,font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: add_to_output(9))
button.pack()
button_label.grid(row=2,column=2,padx=15,pady=15)


# *
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text="*",font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: add_to_output("*"))
button.pack()
button_label.grid(row=2,column=3,padx=15,pady=15)

# C
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text="C",font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: clear_output())
button.pack()
button_label.grid(row=3,column=0,padx=15,pady=15)

# 0
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text="0",font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: add_to_output("0"))
button.pack()
button_label.grid(row=3,column=1,padx=15,pady=15)

# /
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text="/",font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: add_to_output("/"))
button.pack()
button_label.grid(row=3,column=2,padx=15,pady=15)

# =
button_label = Label(frame,bd=0.8,bg="black")
button = Button(button_label,text="=",font=("Arial", 14),fg="blue",bg="light gray",relief="flat",height=2,width=5,command=lambda: calculate_output())
button.pack()
button_label.grid(row=3,column=3,padx=15,pady=15)


# Execution 
window.mainloop()

