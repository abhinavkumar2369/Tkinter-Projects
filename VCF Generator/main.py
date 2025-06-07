# ------------------- Import ----------------------
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox



# -------------------- Window ----------------------
window = tk.Tk()
window.title("VCF Generator")
window.geometry("900x600")
window.resizable(True, True)
window.config(background="#daf7e4")
window.minsize(900, 600)
logo = PhotoImage(file='logo.png')
window.iconphoto(False, logo)



# Ensure High DPI awareness on Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass



# -------------- Data  &  Function  -----------------
data = []

def submit():
    global data
    name = name_value.get()
    phone_no = phone_no_value.get()
    email = email_value.get()
    data.append([name, phone_no, email])
    table.insert(parent= "", index=0, values=(name, phone_no, email))
    print(data)
    
def generate_vcf():
    with open("contacts.vcf", "w") as file:
        for i in data:
            file.write("BEGIN:VCARD\n")
            file.write("VERSION:3.0\n")
            file.write(f"N:{i[0]}\n")
            file.write(f"FN:{i[0]}\n")
            file.write(f"TEL;TYPE=CELL:{i[1]}\n")
            file.write(f"EMAIL:{i[2]}\n")
            file.write("END:VCARD\n")
        file.close()
    print("VCF File Generated")
    print("Contacts.vcf file is generated successfully")
    tk.messagebox.showinfo("Success", "Contacts.vcf file is generated successfully")


def print_table(lower_frame):
    global table
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 15))
    style.configure("Treeview", font=("Arial", 12))
    table = ttk.Treeview(lower_frame, columns=("Name", "Phone No", "Email"), show="headings", height=10)
    scrollbar = ttk.Scrollbar(table, orient="vertical", command=table.yview)
    scrollbar.pack(side="right", fill="y")
    table.configure(yscrollcommand=table.yview)
    table.heading("Name", text="Name")
    table.heading("Phone No", text="Phone No")
    table.heading("Email", text="Email")
    for i in data:
        table.insert(parent= "", index=0, values=(i[0], i[1], i[2]))
    table.pack(fill="both", expand=True, pady=(40,40),padx=(20,20))



# --------------------- Heading ----------------------

heading = tk.Label(window, text="VCF  Generator", font=("Arial", 24),bg="white",background="#e7d7fc",pady=20)
heading.pack(fill="x")




# ---------------------- Frames ----------------------

upper_frame = tk.Frame(window, bg="#daf7e4", pady=20,height=100)
lower_frame = tk.Frame(window, bg="#daf7e4")
upper_frame.pack()
lower_frame.pack(fill="both",expand=True)




# --------------------- Left Frame -------------------

## Name
name_label = tk.Label(upper_frame, text="Name:",height=2, width=10,background="#daf7e4",font=("Arial", 16))
name_value = tk.Entry(upper_frame,  border=1, highlightthickness=1, highlightbackground="lightgray",font=("Arial", 14))
name_label.grid(row=0, column=0,padx=10,pady=10)
name_value.grid(row=1, column=0,padx=10,pady=10)



# ----------------------------------------------------

# Phone No
phone_no_label = tk.Label(upper_frame, text="Phone No:",height=2, width=10,background="#daf7e4",font=("Arial", 16))
phone_no_value = tk.Entry(upper_frame,  border=1, highlightthickness=1, highlightbackground="lightgray",font=("Arial", 14))
phone_no_label.grid(row=0, column=1, padx=10,pady=10)
phone_no_value.grid(row=1, column=1, padx=10,pady=10)


# Email
email_label = tk.Label(upper_frame, text="Email:",height=2, width=10,background="#daf7e4",font=("Arial", 16))
email_value = tk.Entry(upper_frame, border=1, highlightthickness=1, highlightbackground="lightgray",font=("Arial", 14))
email_label.grid(row=0, column=2,padx=10,pady=10)
email_value.grid(row=1, column=2,padx=10,pady=10)



style = ttk.Style()
style.configure("MyButton.TButton", font=("Arial", 14),padding=3)



#Submit Button
submit_button = ttk.Button(upper_frame, text="Submit", command=submit,style="MyButton.TButton")
submit_button.grid(row=2, column=1, padx=10,pady=10)

# Generate VCF Button
generate_vcf_button = ttk.Button(upper_frame, text="Generate VCF", command=generate_vcf,style="MyButton.TButton")
generate_vcf_button.grid(row=2, column=2, padx=10,pady=10)

# -----------------------------------------------------

print_table(lower_frame)

window.mainloop()

