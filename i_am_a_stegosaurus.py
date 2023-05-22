import os
import tkinter as tk
from tkinter import Label, Text, Button, messagebox, Frame, Scrollbar, IntVar, Checkbutton, Spinbox
from tkinterdnd2 import DND_FILES, Tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import cv2


def encode(path, bit, text):
    print('encode png at', path, 'with', bit, 'bit and text =', text)


def decode(path, bit):
    print('decode png', path, 'with', bit, 'bit')


supported_types = {
    '.png': (encode, decode),
    '.gif': None,
    '.bmp': None,
    '.wav': None,
    '.mp3': None,
    '.mp4': None,
    '.txt': None,
    '.xls': None,
    '.doc': None
}


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

    if ext.lower() not in list(filetype):
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
        # self.root.geometry('685x500')
        self.root.resizable(0, 0)

        # frame
        self.rootFrame = Frame(self.root)
        self.settingFrame = Frame(self.rootFrame)
        self.settingSubFrame1 = Frame(self.settingFrame)
        self.settingSubFrame2 = Frame(self.settingFrame)
        self.payloadFrame = Frame(self.rootFrame)
        self.coverFrame = Frame(self.rootFrame)
        self.actionFrame = Frame(self.rootFrame)

        self.payloadFrame.drop_target_register(DND_FILES)
        self.payloadFrame.dnd_bind('<<Drop>>', self.payload_on_drop)

        self.coverFrame.drop_target_register(DND_FILES)
        self.coverFrame.dnd_bind('<<Drop>>', self.cover_on_drop)

        self.rootFrame.pack(padx=10, pady=10)
        self.settingFrame.pack(anchor='w', padx=(0, 10), pady=(0, 10))
        self.settingSubFrame1.grid(row=1, column=0, sticky='w', pady=(0, 10))
        self.settingSubFrame2.grid(row=2, column=0, sticky='w', pady=(0, 10))
        self.payloadFrame.pack(anchor='w', padx=(0, 10), pady=(0, 10))
        self.coverFrame.pack(anchor='w', padx=(0, 10), pady=(0, 10))
        self.actionFrame.pack(padx=(0, 10), pady=(0, 10))

        # variables
        self.payloadPath = None
        self.coverPath = None
        self.payloadText = None

        # setting frame
        Label(self.settingFrame, text="Settings", font=('Aria', 10)).grid(row=0, column=0, sticky='w')
        self.ckbSaveOptionVar = IntVar()
        Checkbutton(self.settingSubFrame1, text="Save decoded text",
                    variable=self.ckbSaveOptionVar).grid(row=0, column=0, sticky='w')
        self.sbNumBit = Spinbox(self.settingSubFrame1, from_=1, to=5)
        Label(self.settingSubFrame1, text="Number of bits:").grid(row=0, column=1, padx=(20, 0))
        self.sbNumBit.grid(row=0, column=2)
        Label(self.settingSubFrame2, text="Password:").grid(row=0, column=0, sticky='w')
        txt_password = Text(self.settingSubFrame2, height=1, width=72)
        txt_password.grid(row=0, column=1, sticky='w')

        # payload frame
        Label(self.payloadFrame, text="Payload", font=('Aria', 10)).grid(row=0, column=0, sticky='w')
        Button(self.payloadFrame, text="Upload a payload file or drag and drop here",
               command=self.payload_on_change, width=90).grid(row=1, column=0, pady=(0, 10))
        self.payload_scroll_bar = Scrollbar(self.payloadFrame)
        self.payload_scroll_bar.grid(row=2, column=1, sticky='nse')
        self.payload_text = Text(self.payloadFrame, height=5, yscrollcommand=self.payload_scroll_bar.set)
        self.payload_text.grid(row=2, column=0, sticky='w')

        # cover frame
        Label(self.coverFrame, text="Cover", font=('Aria', 10)).grid(row=0, column=0, sticky='w')
        Button(self.coverFrame, text="Upload a cover file or drag and drop here",
               command=self.cover_on_change, width=90).grid(row=1, column=0, pady=(0, 10))

        # action frame
        Button(self.actionFrame, text="Encode", command=self.encode).grid(row=0, column=0, sticky='e', padx=(0, 10))
        Button(self.actionFrame, text="Decode", command=self.decode).grid(row=0, column=1, sticky='w', padx=(10, 0))

    def payload_on_change(self):
        self.payloadPath = get_path([('Text file', '*.txt')])
        if self.payloadPath is not None:
            self.show_payload()

    def payload_on_drop(self, event):
        self.payloadPath = get_drop(event, {'.txt'})
        if self.payloadPath is not None:
            self.show_payload()

    def show_payload(self):
        self.payload_text.delete('1.0', tk.END)
        self.payloadText = get_text_content(self.payloadPath)
        self.payload_text.insert('1.0', self.payloadText)

    def cover_on_change(self):
        self.coverPath = get_path([('', '*' + key) for key in supported_types.keys()])
        if self.coverPath is not None:
            self.show_cover()

    def cover_on_drop(self, event):
        self.coverPath = get_drop(event, supported_types)
        if self.coverPath is not None:
            self.show_cover()

    def show_cover(self):
        os.startfile(self.coverPath)

    def encode(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Please select or drop a cover item first!")
            return
        _, ext = os.path.splitext(self.coverPath)
        self.payloadText = self.payload_text.get('1.0', 'end-1c')
        supported_types[ext.lower()][0](self.coverPath, int(self.sbNumBit.get()), self.payloadText)

    def decode(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Please select or drop a cover item first!")
            return
        _, ext = os.path.splitext(self.coverPath)
        supported_types[ext.lower()][1](self.coverPath, int(self.sbNumBit.get()))

    def run(self):
        self.root.mainloop()


app().run()
