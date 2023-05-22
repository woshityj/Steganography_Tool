import os
import tkinter as tk
from tkinter import Label, Text, Button, messagebox, Frame, Scrollbar
from tkinterdnd2 import DND_FILES, Tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import cv2

supported_types = (
    '.png',
    '.gif',
    '.bmp',
    '.wav',
    '.mp3',
    '.mp4',
    '.txt',
    '.xls',
    '.doc'
)

def get_path(filetype):
    file_path = askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetype
    )
    if file_path:
        return file_path


def get_drop(event, filetype):
    file_path = event.data
    if os.path.isfile(file_path):
        _, ext = os.path.splitext(file_path)
    else:
        messagebox.showerror("Error", f"Cannot open file from {file_path}")
        return

    if ext.lower() not in filetype:
        messagebox.showerror("Error", f"File type {ext} not supported.")
        return
    return file_path


def get_text_content(path):
    with open(path, 'r') as file:
        return file.read()


class app:
    def __init__(self):
        # UI
        self.root = Tk()
        self.root.title("i_am_a_stegosaurus")
        self.root.geometry('685x500')
        self.root.resizable(0, 0)

        # frame
        self.rootFrame = Frame(self.root)
        self.settingFrame = Frame(self.rootFrame)
        self.payloadFrame = Frame(self.rootFrame)
        self.coverFrame = Frame(self.rootFrame)

        self.payloadFrame.drop_target_register(DND_FILES)
        self.payloadFrame.dnd_bind('<<Drop>>', self.payload_on_drop)

        self.coverFrame.drop_target_register(DND_FILES)
        self.coverFrame.dnd_bind('<<Drop>>', self.cover_on_drop)

        self.rootFrame.pack(padx=10, pady=10)
        self.settingFrame.pack(anchor='w', padx=(0, 10), pady=(0, 10))
        self.payloadFrame.pack(anchor='w', padx=(0, 10), pady=(0, 10))
        self.coverFrame.pack(anchor='w', padx=(0, 10), pady=(0, 10))

        # variables
        self.payloadPath = None
        self.coverPath = None

        # setting frame
        Label(self.settingFrame, text="Settings", font=('Aria', 10)).grid(row=0, column=0, sticky='w')
        # self.ckbSaveOptionVar = IntVar()
        # Checkbutton(self.settingFrame, text="Show files after execution",
        #             variable=self.ckbSaveOptionVar).grid(row=1, column=0, sticky='w')
        Label(self.settingFrame, text="Password:").grid(row=2, column=0, sticky='w')
        txt_password = Text(self.settingFrame, height=1, width=72)
        txt_password.grid(row=2, column=1, sticky='w')

        # payload frame
        Label(self.payloadFrame, text="Payload", font=('Aria', 10)).grid(row=0, column=0, sticky='w')
        Button(self.payloadFrame, text="Upload a payload file or drag and drop here",
               command=self.payload_on_change, width=91).grid(row=1, column=0)
        self.payload_scroll_bar = Scrollbar(self.payloadFrame)
        self.payload_scroll_bar.grid(row=2, column=1, sticky='nse')
        self.payload_text = Text(self.payloadFrame, height=5, yscrollcommand=self.payload_scroll_bar.set)
        self.payload_text.grid(row=2, column=0, sticky='w')

        # cover frame
        Label(self.coverFrame, text="Cover", font=('Aria', 10)).grid(row=0, column=0, sticky='w')
        Button(self.coverFrame, text="Upload a cover file or drag and drop here",
               command=self.cover_on_change, width=91).grid(row=1, column=0)

    def payload_on_change(self):
        self.payloadPath = get_path([('Text file', '*.txt')])
        if self.payloadPath is not None:
            self.show_payload()

    def payload_on_drop(self, event):
        self.payloadPath = get_drop(event, '.txt')
        if self.payloadPath is not None:
            self.show_payload()

    def show_payload(self):
        self.payload_text.delete('1.0', tk.END)
        self.payload_text.insert('1.0', get_text_content(self.payloadPath))

    def cover_on_change(self):
        self.coverPath = get_path([('All file', '*.*')])
        if self.coverPath is not None:
            self.show_cover()

    def cover_on_drop(self, event):
        self.coverPath = get_drop(event, supported_types)
        if self.coverPath is not None:
            self.show_cover()

    def show_cover(self):
        os.startfile(self.coverPath)

    def run(self):
        self.root.mainloop()


app().run()
