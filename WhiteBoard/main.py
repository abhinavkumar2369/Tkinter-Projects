import tkinter as tk
from tkinter import colorchooser, PhotoImage
from PIL import Image, ImageTk
import os



# Ensure High DPI awareness on Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


        
def setup_whiteboard():
    root = tk.Tk()
    root.title("Simple Whiteboard")
    root.resizable(False, False)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo = PhotoImage(file=os.path.join(current_dir, 'images/logo.png'))
    root.iconphoto(False, logo)
    
    canvas = tk.Canvas(root, width=800, height=600, bg="white")
    canvas.pack()
    
    return root, canvas



def setup_tools(root, canvas):
    tools_frame = tk.Frame(root)
    tools_frame.pack(side=tk.TOP, fill=tk.X)
    
    current_color = tk.StringVar(value="black")
    current_tool = tk.StringVar(value="pencil")
    line_width = tk.IntVar(value=2)
    
    pencil_img = Image.open("images/pencil_cursor.png")
    pencil_img = pencil_img.resize((32, 32), Image.LANCZOS)
    pencil_cursor = ImageTk.PhotoImage(pencil_img)
    
    eraser_img = Image.open("images/eraser_cursor.png")
    eraser_img = eraser_img.resize((32, 32), Image.LANCZOS)
    eraser_cursor = ImageTk.PhotoImage(eraser_img)
    
    cursor_item = None
    
    def use_pencil():
        current_tool.set("pencil")
        update_cursor(pencil_cursor)
    
    def use_eraser():
        current_tool.set("eraser")
        update_cursor(eraser_cursor)
    
    def update_cursor(cursor_image):
        nonlocal cursor_item
        if cursor_item:
            canvas.delete(cursor_item)
        canvas.config(cursor="none")
        cursor_item = canvas.create_image(0, 0, image=cursor_image, anchor=tk.NW)
        move_cursor(None)
    
    def change_color():
        color = colorchooser.askcolor(title="Choose color")[1]
        if color:
            current_color.set(color)
    
    def change_width(value):
        line_width.set(int(value))
    
    def move_cursor(event):
        if cursor_item:
            x = canvas.winfo_pointerx() - canvas.winfo_rootx()
            y = canvas.winfo_pointery() - canvas.winfo_rooty()
            canvas.coords(cursor_item, x, y)
    
    tk.Button(tools_frame, text="Pencil", command=use_pencil).pack(side=tk.LEFT, padx=5)
    tk.Button(tools_frame, text="Eraser", command=use_eraser).pack(side=tk.LEFT, padx=5)
    tk.Button(tools_frame, text="Color", command=change_color).pack(side=tk.LEFT, padx=5)
    tk.Scale(tools_frame, from_=1, to=10, orient=tk.HORIZONTAL, label="Width", command=change_width).pack(side=tk.LEFT, padx=5)
    
    canvas.bind("<Motion>", move_cursor)
    
    # Initial cursor
    use_pencil()
    
    return current_color, current_tool, line_width, pencil_cursor, eraser_cursor



def setup_drawing(canvas, current_color, current_tool, line_width):
    last_x, last_y = None, None
    
    def on_mouse_press(event):
        nonlocal last_x, last_y
        last_x, last_y = event.x, event.y
    
    def on_mouse_move(event):
        nonlocal last_x, last_y
        if last_x and last_y:
            if current_tool.get() == "eraser":
                canvas.create_line(last_x, last_y, event.x, event.y, 
                                   width=line_width.get(), fill="white", 
                                   capstyle=tk.ROUND, smooth=tk.TRUE)
            else:
                canvas.create_line(last_x, last_y, event.x, event.y, 
                                   width=line_width.get(), fill=current_color.get(), 
                                   capstyle=tk.ROUND, smooth=tk.TRUE)
            last_x, last_y = event.x, event.y
    
    def on_mouse_release(event):
        nonlocal last_x, last_y
        last_x, last_y = None, None
    
    canvas.bind("<Button-1>", on_mouse_press)
    canvas.bind("<B1-Motion>", on_mouse_move)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)



def main():
    root, canvas = setup_whiteboard()
    current_color, current_tool, line_width, pencil_cursor, eraser_cursor = setup_tools(root, canvas)
    setup_drawing(canvas, current_color, current_tool, line_width)
    root.mainloop()



if __name__ == "__main__":
    main()