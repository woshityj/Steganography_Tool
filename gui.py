import os
import tkinter as tk
import wave
from tkinter import Label, Text, Button, messagebox, Frame, Scrollbar, IntVar, Checkbutton, Spinbox, Canvas
from PIL import Image, ImageTk

import cv2
from tkinterdnd2 import DND_FILES, Tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import image_steganography as ims
import document_steganography as dms
import audio_steganography as auds

import math

supported_types = {
    '.png': (ims.encode, ims.decode),
    '.gif': None,
    '.bmp': None,
    '.wav': None,
    '.mp3': None,
    '.mp4': None,
    '.txt': (dms.decode),
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

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):

        # variables
        self.payloadPath = None
        self.coverPath = None
        self.payloadText = None
        self.encoded = None

        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('450x300')

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (MainMenu, ImagePage, DocumentPage, AudioPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(MainMenu)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        # UI
        tk.Frame.__init__(self, parent)

        self.label = Label(self, text = "Are you a geek?")
        self.label.grid()

        self.button = Button(self, text="Image Steganography", command = lambda : controller.show_frame(ImagePage))
        self.button.grid(column=1, row=0)

        self.button = Button(self, text="Document Steganography", command = lambda : controller.show_frame(DocumentPage))
        self.button.grid(column=1, row=1)

        self.button = Button(self, text="Audio Steganography", command = lambda : controller.show_frame(AudioPage))
        self.button.grid(column=1, row=2)

    
    def image_steganography(self):
        self.label.configure(text = "I just got clicked")

class ImagePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # input text box for entering secret
        self.lbl_secret = tk.Label(self, text='Secret message: ')
        self.lbl_secret.grid(row=0, column=0, sticky='ne')
        self.tb_message = tk.Text(self, height=2, width=30)
        self.tb_message.grid(row=0, column=1, sticky='w')

        # specify number of LSB
        self.lbl_num = tk.Label(self, text='Number of bits: ')
        self.lbl_num.grid(row=1, column=0, sticky='e')
        self.sb_num = tk.Spinbox(self, from_=1, to=5, width=10)
        self.sb_num.grid(row=1, column=1, sticky='w')

        self.upload_button = Button(self, text="Click here to upload an Image", command=self.cover_on_change)
        self.upload_button.grid(row=1, column = 1)

        self.encode_button = Button(self, text="Encode Image", command = self.encode_image)
        self.encode_button.grid(row = 2, column = 0)

        self.decode_button = Button(self, text="Decode Image", command = self.decode_image)
        self.decode_button.grid(row = 2, column = 1)

    def cover_on_change(self):
        self.coverPath = get_path([('', '*' + key) for key in supported_types.keys()])
        if self.coverPath is not None:
            self.img_before = Label(self, text = "Uploaded Image: ")
            self.img_before.grid(row = 3, column = 0)

            img = Image.open(self.coverPath)
            img = img.resize((100, 100), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.image_label = Label(self, image = img)
            self.image_label.image = img
            self.image_label.grid(row=4, column = 0)
    
    def encode_image(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Please select or drop a cover item first!")
            return
        _, ext = os.path.splitext(self.coverPath)
        self.payloadText = self.tb_message.get('1.0', 'end-1c')
        self.encoded = supported_types[ext.lower()][0](self.coverPath, self.payloadText, int(self.sb_num.get()))
        self.save_as(ext)

    def decode_image(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Please select or drop a cover item first!")
            return
        _, ext = os.path.splitext(self.coverPath)
        text = supported_types[ext.lower()][1](self.coverPath, int(self.sb_num.get()))
        self.tb_message.delete('1.0', tk.END)
        self.tb_message.insert('1.0', text)

        if self.image_label_after is not None:
            self.image_label_after.destroy()

    def save_as(self, ext):
        # save as prompt
        filename = asksaveasfilename(defaultextension=ext, filetypes=[("Same as original", ext), ("All Files", "*.*")])
        if filename:
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                # save image
                cv2.imwrite(filename, self.encoded)
                # show image as per requested in spec
                self.img_after = Label(self, text = "Encoded Image: ")
                self.img_after.grid(row = 3, column = 1)

                img = Image.open(filename)
                img = img.resize((100, 100), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                self.image_label_after = Label(self, image = img)
                self.image_label_after.image = img
                self.image_label_after.grid(row=4, column=1)


class DocumentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # input text box for entering secret
        self.lbl_secret = tk.Label(self, text='Secret message: ')
        self.lbl_secret.grid(row=0, column=0, sticky='ne')
        self.tb_message = tk.Text(self, height=2, width=30)
        self.tb_message.grid(row=0, column=1, sticky='w')

        self.upload_button = Button(self, text="Click here to upload a Document file", command=self.cover_on_change)
        self.upload_button.grid(row=1, column = 1)

        self.encode_button = Button(self, text="Encode Document", command = self.encode_document)
        self.encode_button.grid(row = 2, column = 0)

        self.decode_button = Button(self, text="Decode Document", command=self.decode_document)
        self.decode_button.grid(row = 2, column = 1)
    
    def cover_on_change(self):
        self.coverPath = get_path([('', '*' + key) for key in supported_types.keys()])
        if self.coverPath is not None:
            self.success_label = Label(self, text="Successfully uploaded file")
            self.success_label.grid(row = 3, column = 1)
    
    def encode_document(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Please select or drop a cover item first!")
            return
        _, ext = os.path.splitext(self.coverPath)
        self.payloadText = self.tb_message.get('1.0', 'end-1c')
        secret_text = dms.secret(self.payloadText)
        self.save_as(ext, secret = secret_text)

    def decode_document(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Please select or drop a cover item first!")
            return
        text = dms.decode(self.coverPath)
        self.tb_message.delete('1.0', tk.END)
        self.tb_message.insert('1.0', text)
    
    def save_as(self, ext, secret = None):
        # save as prompt
        filename = asksaveasfilename(defaultextension=ext, filetypes=[("Same as original", ext), ("All Files", "*.*")])
        if filename:
            if filename.endswith(('.txt')):
                dms.encode(self.coverPath, filename, secret)
                print("\nEncoded the data successfully in the document file")


class AudioPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # input text box for entering secret
        self.lbl_secret = tk.Label(self, text='Secret message: ')
        self.lbl_secret.grid(row=0, column=0, sticky='ne')
        self.tb_message = tk.Text(self, height=2, width=30)
        self.tb_message.grid(row=0, column=1, sticky='w')

        self.upload_button = Button(self, text="Click here to upload a Audio file", command=self.cover_on_change)
        self.upload_button.grid(row=1, column = 1)

        self.encode_button = Button(self, text="Encode Audio", command = self.encode_audio)
        self.encode_button.grid(row = 2, column = 0)

        self.decode_button = Button(self, text="Decode Audio", command=self.decode_audio)
        self.decode_button.grid(row = 2, column = 1)

    def cover_on_change(self):
        self.coverPath = get_path([('', '*' + key) for key in supported_types.keys()])
        if self.coverPath is not None:
            self.success_label = Label(self, text="Successfully uploaded file")
            self.success_label.grid(row = 3, column = 1)
    
    def encode_audio(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Please select or drop a cover item first!")
            return
        _, ext = os.path.splitext(self.coverPath)
        self.payloadText = self.tb_message.get('1.0', 'end-1c')
        self.encoded = supported_types[ext.lower()][0](self.coverPath, self.payloadText, int(self.sb_num.get()))
        self.save_as(ext)

    def decode_audio(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Please select or drop a cover item first!")
            return
        text = auds.decode_aud_data(self.coverPath)
        self.tb_message.delete('1.0', tk.END)
        self.tb_message.insert('1.0', text)
    
    def save_as(self, ext, secret = None):
        # save as prompt
        filename = asksaveasfilename(defaultextension=ext, filetypes=[("Same as original", ext), ("All Files", "*.*")])
        if filename:
            if filename.endswith(('.wav')):
                song = wave.open(self.coverPath, mode = 'rb')
                with wave.open(filename, 'wb') as fd:
                    fd.setparams(song.getparams())
                    fd.writeframes(self.encoded)
                    print("\nEncoded the data successfully in the audio file")


app = tkinterApp()
app.mainloop()