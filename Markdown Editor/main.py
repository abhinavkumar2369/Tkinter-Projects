import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage 
from ttkthemes import ThemedTk
import markdown2
import json
import os
from tkhtmlview import HTMLLabel
import google.generativeai as genai
import threading
from queue import Queue


# ---------------------------------------------

# Ensure High DPI awareness on Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# ----------------------------------------------


# Constants
AUTOSAVE_DELAY = 5000
NOTES_FILE = "notes.json"
DEFAULT_NOTE = """# Welcome to AI Markdown Editor!
## Features:
* **AI Assist**: Press Ctrl+Space for AI suggestions
* **AI Commands**: Type /command to use AI features
* **Smart Complete**: Press Tab after a list item


Available AI Commands:

* /improve - Improve writing style
* /expand - Expand current paragraph
* /summarize - Summarize selected text
* /format - Convert text to proper markdown

Start writing your notes here...
"""


# ---------------- Global variables ---------------
root = None
editor = None
preview = None
notes = {}
current_note = None
note_select = None
ai_queue = Queue()
is_processing = False
ai_status = None
model = None

def setup_ui():
    global root, editor, preview, note_select, current_note, ai_status
    
    root = ThemedTk(theme="arc")
    root.title("Markdown Editor")
    root.geometry("1200x700")
    
    root.resizable(True, True)
    root.minsize(800, 500)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo = PhotoImage(file=os.path.join(current_dir, 'logo.png'))
    root.iconphoto(False, logo)
    
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)


    # --------------- Toolbar ---------------------
    toolbar = ttk.Frame(main_frame)
    toolbar.pack(fill=tk.X, pady=(0, 5))

    current_note = tk.StringVar(value="Default Note")
    note_select = ttk.Combobox(toolbar, textvariable=current_note, values=list(notes.keys()))
    note_select.pack(side=tk.LEFT, padx=5)

    ttk.Button(toolbar, text="New Note", command=new_note).pack(side=tk.LEFT, padx=5)
    ttk.Button(toolbar, text="Delete Note", command=delete_note).pack(side=tk.LEFT, padx=5)

    ai_status = tk.StringVar(value="AI: Ready")
    ttk.Label(toolbar, textvariable=ai_status).pack(side=tk.RIGHT, padx=5)


    # ----------------- AI Commands -------------------
    ai_frame = ttk.LabelFrame(toolbar, text="AI Tools")
    ai_frame.pack(side=tk.LEFT, padx=20, fill=tk.X)
    
    for cmd, text in [("/improve", "Improve"), ("/expand", "Expand"), 
                     ("/summarize", "Summarize"), ("/format", "Format")]:
        ttk.Button(ai_frame, text=text, 
                  command=lambda c=cmd: execute_ai_command(c)).pack(side=tk.LEFT, padx=5)


    # ---------------- Editor and Preview ---------------
    paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
    paned.pack(fill=tk.BOTH, expand=True)
    
    editor_frame = ttk.Frame(paned)
    editor = tk.Text(editor_frame, wrap=tk.WORD, font=("Courier", 12))
    editor.pack(fill=tk.BOTH, expand=True)
    
    preview_frame = ttk.Frame(paned)
    preview = HTMLLabel(preview_frame, background="white", html="")
    preview.pack(fill=tk.BOTH, expand=True)
    
    paned.add(editor_frame)
    paned.add(preview_frame)


def bind_events():
    editor.bind("<KeyRelease>", update_preview)
    editor.bind("<Control-space>", trigger_ai_completion)
    note_select.bind("<<ComboboxSelected>>", lambda e: load_current_note())
    editor.bind("<Return>", check_for_command)
    editor.bind("<Tab>", smart_tab)


def load_notes():
    global notes
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, 'r') as f:
                notes = json.load(f)
        except:
            notes = {"Default Note": DEFAULT_NOTE}
    else:
        notes = {"Default Note": DEFAULT_NOTE}


def save_notes():
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f)


def update_preview(event=None):
    markdown_text = editor.get("1.0", tk.END)
    html = markdown2.markdown(markdown_text)
    styled_html = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px;">
        {html}
    </div>
    """
    preview.set_html(styled_html)


def process_ai_command(command, text):
    prompts = {
        "/improve": "Improve the writing style of the following text while maintaining its meaning:\n",
        "/expand": "Expand the following text with more details and examples:\n",
        "/summarize": "Summarize the following text concisely:\n",
        "/format": "Convert the following text to proper markdown format:\n",
        "/complete": "Complete the following text naturally:\n"
    }
    
    prompt = prompts.get(command, prompts["/improve"]) + text
    response = model.generate_content(prompt)
    return response.text


def execute_ai_command(command):
    if is_processing:
        return        
    try:
        text = editor.get(tk.SEL_FIRST, tk.SEL_LAST)
    except tk.TclError:
        text = get_current_paragraph()
        
    if text.strip():
        ai_queue.put((command, text))


def update_editor_with_ai_result(result):
    try:
        start = editor.index(tk.SEL_FIRST)
        end = editor.index(tk.SEL_LAST)
    except tk.TclError:
        start = editor.index("insert linestart")
        end = editor.index("insert lineend")
        
    editor.delete(start, end)
    editor.insert(start, result)
    update_preview()


def get_current_paragraph():
    start = editor.index("insert linestart")
    end = editor.index("insert lineend")
    return editor.get(start, end)


def trigger_ai_completion(event=None):
    if is_processing:
        return "break"
        
    insert_pos = editor.index("insert")
    start = editor.index(f"{insert_pos} linestart-5lines")
    context = editor.get(start, insert_pos)
    
    ai_queue.put(("/complete", context))
    return "break"


def smart_tab(event=None):
    insert_pos = editor.index("insert linestart")
    line = editor.get(insert_pos, "insert lineend")
    
    if line.strip().startswith(('- ', '* ', '1. ')):
        editor.insert("insert", "\n" + line.split()[0] + " ")
        return "break"
    return None


def check_for_command(event=None):
    insert_pos = editor.index("insert linestart")
    line = editor.get(insert_pos, "insert lineend")
    
    if line.strip().startswith('/'):
        command = line.strip()
        execute_ai_command(command)
        return "break"
    return None


def new_note():
    name = f"Note {len(notes) + 1}"
    notes[name] = ""
    note_select['values'] = list(notes.keys())
    current_note.set(name)
    load_current_note()


def delete_note():
    if len(notes) > 1:
        del notes[current_note.get()]
        note_select['values'] = list(notes.keys())
        current_note.set(list(notes.keys())[0])
        load_current_note()
        save_notes()
    else:
        messagebox.showwarning("Warning", "Cannot delete the last note!")


def load_current_note():
    editor.delete("1.0", tk.END)
    editor.insert("1.0", notes[current_note.get()])
    update_preview()


def schedule_autosave():
    if editor.edit_modified():
        notes[current_note.get()] = editor.get("1.0", tk.END.strip())
        save_notes()
        editor.edit_modified(False)
    root.after(AUTOSAVE_DELAY, schedule_autosave)


def start_ai_worker():
    def worker():
        global is_processing
        while True:
            try:
                command, text = ai_queue.get()
                if command is None:
                    break
                    
                is_processing = True
                ai_status.set("AI: Processing...")
                result = process_ai_command(command, text)
                root.after(0, update_editor_with_ai_result, result)
                
            except Exception as e:
                root.after(0, messagebox.showerror, "AI Error", str(e))
            finally:
                is_processing = False
                ai_status.set("AI: Ready")
                ai_queue.task_done()
                
    ai_thread = threading.Thread(target=worker, daemon=True)
    ai_thread.start()


def main():
    global model
    genai.configure(api_key="------- YOUR GEMINI API KEY HERE -------")
    model = genai.GenerativeModel('gemini-pro')
    
    load_notes()
    setup_ui()
    bind_events()
    start_ai_worker()
    load_current_note()
    schedule_autosave()
    root.mainloop()


if __name__ == "__main__":
    main()