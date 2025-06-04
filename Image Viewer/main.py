import tkinter as tk
from tkinter import filedialog, ttk, PhotoImage
from PIL import Image, ImageTk
from datetime import datetime
import os


# --------------------------------------------------

# Ensure High DPI awareness on Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# --------------------------------------------------


def select_image():
    global img_label, current_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    if file_path:
        status_label.config(text=f"Selected: {os.path.basename(file_path)}")
        
        current_image = Image.open(file_path)
        display_image()


def display_image():
    global img_label, current_image
    frame_width = image_frame.winfo_width()
    frame_height = image_frame.winfo_height()
    
    img_copy = current_image.copy()
    ratio = min(frame_width/img_copy.width, frame_height/img_copy.height)
    new_width = int(img_copy.width * ratio)
    new_height = int(img_copy.height * ratio)
    img_copy = img_copy.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    photo = ImageTk.PhotoImage(img_copy)
    img_label.config(image=photo)
    img_label.image = photo


def on_frame_configure(event):
    if 'current_image' in globals():
        display_image()


root = tk.Tk()
root.title("Modern Image Viewer")
root.geometry("800x600")
root.configure(bg="#2c3e50")
logo = PhotoImage(file='logo.png')
root.iconphoto(False, logo)


style = ttk.Style()
style.configure("TButton", padding=10, font=("Helvetica", 12))
style.configure("TFrame", background="#34495e")

main_container = ttk.Frame(root, style="TFrame")
main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

top_bar = ttk.Frame(main_container, style="TFrame")
top_bar.pack(fill=tk.X, pady=(0, 10))

image_frame = ttk.Frame(main_container, style="TFrame")
image_frame.pack(fill=tk.BOTH, expand=True, pady=10)
image_frame.bind('<Configure>', on_frame_configure)

img_label = tk.Label(image_frame, bg="#34495e")
img_label.pack(expand=True)

bottom_bar = ttk.Frame(main_container, style="TFrame")
bottom_bar.pack(fill=tk.X, pady=(10, 0))

select_btn = tk.Button(
    bottom_bar,
    text="Select Image",
    command=select_image,
    font=("Helvetica", 12, "bold"),
    bg="#3498db",
    fg="white",
    activebackground="#2980b9",
    activeforeground="white",
    relief=tk.FLAT,
    padx=20,
    pady=10
)
select_btn.pack(side=tk.LEFT)

status_label = tk.Label(
    bottom_bar,
    text="No image selected",
    bg="#34495e",
    fg="#ecf0f1",
    font=("Helvetica", 10)
)
status_label.pack(side=tk.RIGHT, padx=10)

current_image = None

root.mainloop()