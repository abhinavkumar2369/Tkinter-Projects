import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from tkinter import PhotoImage

# --------------------------------------------------


# Ensure High DPI awareness on Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


# --------------------------------------------------


# Open File
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            editor.delete('1.0', tk.END)
            editor.insert(tk.END, file.read())


# -------------------------------------------------


# Save File
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(editor.get('1.0', tk.END))


# -------------------------------------------------


def clear_editor():
    editor.delete('1.0', tk.END)


def show_about():
    messagebox.showinfo("About", "Version-1.0.0 \n Designed by Abhinav Kumar")


# -------------------------------------------------


root = tk.Tk()
root.title("Notepad")

logo = PhotoImage(file='logo.png')

# Set the logo as the application icon
root.iconphoto(False, logo)

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Clear", command=clear_editor)

help_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_about )

editor = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
editor.pack(expand=True, fill='both')

root.mainloop()