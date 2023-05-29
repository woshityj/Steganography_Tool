import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import customtkinter
from tkinter.filedialog import asksaveasfilename, askopenfilename
import wave

import cv2
import image_steganography as ims
import document_steganography as dms
import audio_steganography as auds
import gif_steganography as gis
import video_steganography as vids
import word_doc_steganography as wds

supported_types = {
    '.png': (ims.png_encode, ims.png_decode),
    '.gif': (gis.gif_encode, gis.gif_decode),
    '.bmp': (ims.bmp_encode, ims.bmp_decode),
    '.wav': (auds.encode_aud_data, auds.decode_aud_data),
    '.mp3': (auds.encode_aud_data, auds.decode_aud_data),
    '.mp4': (vids.encode_video, vids.decode_video),
    '.txt': (dms.decode),
    '.xls': None,
    '.docx': None
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

class MainMenu(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight = 1)

        # add widgets onto the frame, for example:
        self.label = customtkinter.CTkLabel(self, text = "Steganography", font = customtkinter.CTkFont(size = 20, weight = "bold"))
        self.label.grid(row = 0, column = 0, padx = 20, pady=10)
        self.img_steg_button = customtkinter.CTkButton(self, text = "Image Steganography", command = lambda : controller.show_frame(ImagePage))
        self.img_steg_button.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.doc_steg_button = customtkinter.CTkButton(self, text = "Document Steganography", command = lambda : controller.show_frame(DocumentPage))
        self.doc_steg_button.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.img_steg_button = customtkinter.CTkButton(self, text = "Audio Steganography", command = lambda : controller.show_frame(AudioPage))
        self.img_steg_button.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        self.img_steg_button = customtkinter.CTkButton(self, text = "Video Steganography", command = lambda : controller.show_frame(VideoPage))
        self.img_steg_button.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

class ImagePage(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)

        self.encoded_image_label = None
        self.image_label = customtkinter.CTkLabel(self)
        self.gif_Label = tk.Label(self)

        self.grid_columnconfigure((0, 1), weight = 1)

        self.back_button = customtkinter.CTkButton(self, text = "Back", command = lambda: controller.show_frame(MainMenu))
        self.back_button.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 10)

        self.label = customtkinter.CTkLabel(self, text="Image Steganography", font = customtkinter.CTkFont(size = 20, weight = "bold"))
        self.label.grid(row = 1, column = 0, padx = 20, pady= 10, columnspan = 2)

        self.label = customtkinter.CTkLabel(self, text="Settings", font = customtkinter.CTkFont(size = 20))
        self.label.grid(row = 2, column = 0, padx = 20, pady= 10, columnspan = 2)

        self.label = customtkinter.CTkLabel(self, text="Set Number of Bits", font = customtkinter.CTkFont(size = 15))
        self.label.grid(row = 3, column = 0, padx = 20, pady= 2)
        self.bits_option_menu = customtkinter.CTkOptionMenu(self, values = ["1", "2", "3", "4", "5"])
        self.bits_option_menu.grid(row = 4, column = 0, padx = 20, pady = (10, 10))

        self.checkbox = customtkinter.CTkCheckBox(self, text = "Save Text")
        self.checkbox.grid(row = 4, column = 1, padx = 20, pady = 10)

        self.label = customtkinter.CTkLabel(self, text="Cover", font = customtkinter.CTkFont(size = 20))
        self.label.grid(row = 5, column = 0, padx = 20, pady= 10, columnspan = 2)
        self.upload_button = customtkinter.CTkButton(self, text = "Click here or Drop an Image here to upload an Image", command = self.cover_on_change)
        self.upload_button.grid(row = 6, column = 0, padx = 20, pady = 10, sticky = "ew", columnspan = 2)
        self.upload_button.drop_target_register(DND_FILES)
        self.upload_button.dnd_bind("<<Drop>>", self.cover_on_drop)

        self.label = customtkinter.CTkLabel(self, text="Secret Message", font = customtkinter.CTkFont(size = 20))
        self.label.grid(row = 7, column = 0, padx = 20, pady= 10, columnspan = 2)
        self.secret_message = customtkinter.CTkTextbox(self, height = 100, width = 450)
        self.secret_message.grid(row = 8, column = 0, sticky = 'w', columnspan = 2)

        self.encode_button = customtkinter.CTkButton(self, text = "Encode Image", command = self.encode_image)
        self.encode_button.grid(row = 9, column = 0, padx = 20, pady = 10)

        self.decode_button = customtkinter.CTkButton(self, text = "Decode Image", command = self.decode_image)
        self.decode_button.grid(row = 9, column = 1, padx = 20, pady = 10)

        self.label = customtkinter.CTkLabel(self, text="Uploaded Image", font = customtkinter.CTkFont(size = 20))
        self.label.grid(row = 10, column = 0, padx = 20, pady= 10, columnspan = 1)

        self.label = customtkinter.CTkLabel(self, text="Encoded Image", font = customtkinter.CTkFont(size = 20))
        self.label.grid(row = 10, column = 1, padx = 20, pady= 10, columnspan = 1)

    def cover_on_drop(self, event):
        self.coverPath = get_drop(event, supported_types)
        if self.coverPath is not None:
            self.show(self.coverPath)

    def cover_on_change(self):
        self.coverPath = get_path([('', '*' + key) for key in supported_types.keys()])
        if self.coverPath is not None:
            self.show(self.coverPath)

    def show(self, coverPath):
        if coverPath.lower().endswith(('.png', '.bmp')):
            self.after(0)
            self.gif_Label.grid_forget()
            self.uploaded_image = customtkinter.CTkImage(Image.open(coverPath), size = (100, 100))
            self.image_label = customtkinter.CTkLabel(self, image = self.uploaded_image, text = "")
            self.image_label.grid(row = 11, column = 0)

            self.success_label = customtkinter.CTkLabel(self, text ="Successfully uploaded file")
            self.success_label.grid(row = 12, column = 0)
        if coverPath.lower().endswith('.gif'):
            self.image_label.grid_forget()
            self.gif = Image.open(coverPath)
            self.frames = [tk.PhotoImage(file=coverPath, format='gif -index %i' % i) for i in range(self.gif.n_frames)]
            self.gif_Label = tk.Label(self, image=self.frames[0], text="", height=100, width=100)
            self.gif_Label.grid(row = 11, column = 0)
            self.after(0, self.play_gif, 0)

    def play_gif(self, fn):
        frame = self.frames[fn]
        fn +=1
        if fn == self.gif.n_frames:
            fn = 0
        self.gif_Label.configure(image=frame)
        self.after(self.gif.info['duration'], self.play_gif, fn)

    def encode_image(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Please select or drop a cover item first!")
            return
        _, ext = os.path.splitext(self.coverPath)
        self.payloadText = self.secret_message.get('1.0', 'end-1c')
        if ext.lower() == '.png' or ext.lower() == '.gif':
            self.encoded = supported_types[ext.lower()][0](self.coverPath, self.payloadText, int(self.bits_option_menu.get()))
        elif (ext.lower() == '.bmp'):
            self.encoded = supported_types[ext.lower()][0](self.coverPath, self.payloadText)
        self.save_as(ext)
    
    def decode_image(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Please select or drop a cover item first!")
            return
        _, ext = os.path.splitext(self.coverPath)
        if ext.lower() == '.png' or ext.lower() == '.gif':
            text = supported_types[ext.lower()][1](self.coverPath, int(self.bits_option_menu.get()))
            print(text)
        elif (ext.lower() == '.bmp'):
            text = supported_types[ext.lower()][1](self.coverPath)
        self.secret_message.delete('1.0', tk.END)
        self.secret_message.insert('1.0', text)

        if self.encoded_image_label is not None:
            self.encoded_image_label.destroy()

    def save_as(self, ext):
        # save as prompt
        filename = asksaveasfilename(defaultextension=ext, filetypes=[("Same as original", ext), ("All Files", "*.*")])
        if filename:
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                # save image
                cv2.imwrite(filename, self.encoded)
                # show image as per requested in spec
                self.encoded_image = customtkinter.CTkImage(Image.open(filename), size = (100, 100))
                self.encoded_image_label = customtkinter.CTkLabel(self, image = self.encoded_image, text = "")
                self.encoded_image_label.grid(row = 11, column = 1)
            if filename.endswith('.gif'):
                gis.gif_save(self.encoded, filename)
                # show gif


class DocumentPage(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0, 1), weight = 1)

        self.back_button = customtkinter.CTkButton(self, text = "Back", command = lambda: controller.show_frame(MainMenu))
        self.back_button.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 10)

        self.label = customtkinter.CTkLabel(self, text = "Document Steganography", font = customtkinter.CTkFont(size = 20, weight = "bold"))
        self.label.grid(row = 1, column = 0, padx = 20, pady= 10, columnspan = 2)

        self.label = customtkinter.CTkLabel(self, text="Cover", font = customtkinter.CTkFont(size = 20))
        self.label.grid(row = 2, column = 0, padx = 20, pady= 10, columnspan = 2)
        self.upload_button = customtkinter.CTkButton(self, text = "Click here or Drop an Document here to upload", command = self.cover_on_change)
        self.upload_button.grid(row = 3, column = 0, padx = 20, pady = 10, sticky = "ew", columnspan = 2)
        self.upload_button.drop_target_register(DND_FILES)
        self.upload_button.dnd_bind("<<Drop>>", self.cover_on_drop)

        self.label = customtkinter.CTkLabel(self, text="Secret Message", font = customtkinter.CTkFont(size = 20))
        self.label.grid(row = 4, column = 0, padx = 20, pady= 10, columnspan = 2)
        self.secret_message = customtkinter.CTkTextbox(self, height = 100, width = 450)
        self.secret_message.grid(row = 5, column = 0, sticky = 'w', columnspan = 2)

        self.encode_button = customtkinter.CTkButton(self, text = "Encode Document", command = self.encode_document)
        self.encode_button.grid(row = 6, column = 0, padx = 20, pady = 10)

        self.decode_button = customtkinter.CTkButton(self, text = "Decode Document", command = self.decode_document)
        self.decode_button.grid(row = 6, column = 1, padx = 20, pady = 10)

    def cover_on_drop(self, event):
        self.coverPath = get_drop(event, supported_types)
        if self.coverPath is not None:
            self.success_label = customtkinter.CTkLabel(self, text = "Successfully uploaded file")
            self.success_label.grid(row = 7, column = 0)

    def cover_on_change(self):
        self.coverPath = get_path([('', '*' + key) for key in supported_types.keys()])
        if self.coverPath is not None:
            self.success_label = customtkinter.CTkLabel(self, text = "Successfully uploaded file")
            self.success_label.grid(row = 7, column = 0)
    
    def encode_document(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Please select or drop a cover item first!")
            return
        _, ext = os.path.splitext(self.coverPath)
        print(ext)
        self.payloadText = self.secret_message.get('1.0', 'end-1c')
        if ext == ".docx":
            wds.hiddenParagraphTest(self.coverPath, self.payloadText)
        else:
            secret_text = dms.secret(self.payloadText)
            self.save_as(ext, secret = secret_text)

    def decode_document(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Please select or drop a cover item first!")
            return
        _, ext = os.path.splitext(self.coverPath)
        if ext == ".docx":
            text = wds.findParagraph(self.coverPath)
            self.secret_message.delete('1.0', tk.END)
            self.secret_message.insert('1.0', text)
        else:
            text = dms.decode(self.coverPath)
            self.secret_message.delete('1.0', tk.END)
            self.secret_message.insert('1.0', text)
    
    def save_as(self, ext, secret = None):
        # save as prompt
        filename = asksaveasfilename(defaultextension=ext, filetypes=[("Same as original", ext), ("All Files", "*.*")])
        if filename:
            if filename.endswith(('.txt')):
                dms.encode(self.coverPath, filename, secret)
                print("\nEncoded the data successfully in the document file")
    
class AudioPage(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0, 1), weight = 1)

        self.back_button = customtkinter.CTkButton(self, text = "Back", command = lambda: controller.show_frame(MainMenu))
        self.back_button.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 10)

        self.label = customtkinter.CTkLabel(self, text="Audio Steganography", font = customtkinter.CTkFont(size = 20, weight = "bold"))
        self.label.grid(row = 1, column = 0, padx = 20, pady = 10, columnspan = 2)

        self.label = customtkinter.CTkLabel(self, text="Cover", font = customtkinter.CTkFont(size = 20))
        self.label.grid(row = 2, column = 0, padx = 20, pady= 10, columnspan = 2)
        self.upload_button = customtkinter.CTkButton(self, text = "Click here or Drop an Document here to upload", command = self.cover_on_change)
        self.upload_button.grid(row = 3, column = 0, padx = 20, pady = 10, sticky = "ew", columnspan = 2)
        self.upload_button.drop_target_register(DND_FILES)
        self.upload_button.dnd_bind("<<Drop>>", self.cover_on_drop)

        self.label = customtkinter.CTkLabel(self, text="Secret Message", font = customtkinter.CTkFont(size = 20))
        self.label.grid(row = 4, column = 0, padx = 20, pady= 10, columnspan = 2)
        self.secret_message = customtkinter.CTkTextbox(self, height = 100, width = 450)
        self.secret_message.grid(row = 5, column = 0, sticky = 'w', columnspan = 2)

        self.encode_button = customtkinter.CTkButton(self, text = "Encode Audio", command = self.encode_audio)
        self.encode_button.grid(row = 6, column = 0, padx = 20, pady = 10)

        self.decode_button = customtkinter.CTkButton(self, text = "Decode Audio", command = self.decode_audio)
        self.decode_button.grid(row = 6, column = 1, padx = 20, pady = 10)

    def cover_on_drop(self, event):
        self.coverPath = get_drop(event, supported_types)
        if self.coverPath is not None:
            self.success_label = customtkinter.CTkLabel(self, text = "Successfully uploaded file")
            self.success_label.grid(row = 7, column = 0)

    def cover_on_change(self):
        self.coverPath = get_path([('', '*' + key) for key in supported_types.keys()])
        if self.coverPath is not None:
            self.success_label = customtkinter.CTkLabel(self, text = "Successfully uploaded file")
            self.success_label.grid(row = 7, column = 0)

    def encode_audio(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Please select or drop a cover item first!")
            return
        _, ext = os.path.splitext(self.coverPath)
        self.payloadText = self.secret_message.get('1.0', 'end-1c')
        self.encoded = supported_types[ext.lower()][0](self.coverPath, self.payloadText)
        self.save_as(ext)

    def decode_audio(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Please select or drop a cover item first!")
            return
        text = auds.decode_aud_data(self.coverPath)
        _, ext = os.path.splitext(self.coverPath)
        os.remove(_ + ".wav")
        self.secret_message.delete('1.0', tk.END)
        self.secret_message.insert('1.0', text)

    def save_as(self, ext, secret = None):
        # save as prompt
        filename = asksaveasfilename(defaultextension='wav', filetypes=[("Same as original", 'wav'), ("All Files", "*.*")])
        print(ext)
        if filename:
            if filename.endswith(('.wav')) and ext != ".mp3":
                song = wave.open(self.coverPath, mode = 'rb')
                with wave.open(filename, 'wb') as fd:
                    fd.setparams(song.getparams())
                    fd.writeframes(self.encoded)
                    print("\nEncoded the data successfully in the audio file")
            elif ext == ".mp3":
                _, ext = os.path.splitext(filename)
                temp_file_name, ext = os.path.splitext(self.coverPath)
                song = wave.open(temp_file_name + ".wav", mode = 'rb')
                with wave.open(filename, 'wb') as fd:
                    fd.setparams(song.getparams())
                    fd.writeframes(self.encoded)
                    print("\nEncoded the data successfully in the audio file")
                auds.convertWAVToMP3(filename)
                os.remove(filename)
                os.remove(temp_file_name + ".wav")

class VideoPage(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0, 1), weight = 1)

        self.back_button = customtkinter.CTkButton(self, text = "Back", command = lambda: controller.show_frame(MainMenu))
        self.back_button.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 10)

        self.label = customtkinter.CTkLabel(self, text = "Video Steganography", font = customtkinter.CTkFont(size = 20, weight = "bold"))
        self.label.grid(row = 1, column = 0, padx = 20, pady = 10, columnspan = 2)

        self.label = customtkinter.CTkLabel(self, text = "Settings", font = customtkinter.CTkFont(size = 20))
        self.label.grid(row = 2, column = 0, padx = 20, pady = 10, columnspan = 2)

        self.label = customtkinter.CTkLabel(self, text = "Set Frame Number to Encode Secret in", font = customtkinter.CTkFont(size = 15))
        self.label.grid(row = 3, column = 0, padx = 5, pady = 2)
        self.frame_option = customtkinter.CTkEntry(self, placeholder_text="Frame Number")
        self.frame_option.grid(row = 4, column = 0, padx = 5, pady = (10, 10))

        self.label = customtkinter.CTkLabel(self, text = "Set Number of Bits", font = customtkinter.CTkFont(size = 15))
        self.label.grid(row = 3, column = 1, padx = 5, pady = 2)
        self.bits_option_menu = customtkinter.CTkOptionMenu(self, values = ["1", "2", "3", "4", "5"])
        self.bits_option_menu.grid(row = 4, column = 1, padx = 5, pady = (10, 10))

        self.label = customtkinter.CTkLabel(self, text = "Cover", font = customtkinter.CTkFont(size = 20))
        self.label.grid(row = 5, column = 0, padx = 20, pady = 10, columnspan = 2)
        self.upload_button = customtkinter.CTkButton(self, text = "Click here or Drop a Video here to upload", command = self.cover_on_change)
        self.upload_button.grid(row = 6, column = 0, padx = 20, pady = 10, sticky = "ew", columnspan = 2)
        self.upload_button.drop_target_register(DND_FILES)
        self.upload_button.dnd_bind("<<Drop>>", self.cover_on_drop)

        self.label = customtkinter.CTkLabel(self, text = "Secret Message", font = customtkinter.CTkFont(size = 20))
        self.label.grid(row = 7, column = 0, padx = 20, pady = 10, columnspan = 2)
        self.secret_message = customtkinter.CTkTextbox(self, height = 100, width = 450)
        self.secret_message.grid(row = 8, column = 0, sticky = 'w', columnspan = 2)

        self.encode_button = customtkinter.CTkButton(self, text = "Encode Video", command = self.encode_video)
        self.encode_button.grid(row = 9, column = 0, padx = 20, pady = 10)

        self.decode_button = customtkinter.CTkButton(self, text = "Decode Video", command = self.decode_video)
        self.decode_button.grid(row = 9, column = 1, padx = 20, pady = 10)

    def cover_on_drop(self, event):
        self.coverPath = get_drop(event, supported_types)
        if self.coverPath is not None:
            self.success_label = customtkinter.CTkLabel(self, text = "Successfully uploaded file")
            self.success_label.grid(row = 10, column = 0)
    
    def cover_on_change(self):
        self.coverPath = get_path(['', '*' + key] for key in supported_types.keys())
        if self.coverPath is not None:
            self.success_label = customtkinter.CTkLabel(self, text = "Successfully uploaded file")
            self.success_label.grid(row = 10, column = 0)
    
    def encode_video(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Pleae select or drop a cover item first!")
            return
        _, ext = os.path.splitext(self.coverPath)
        self.payloadText = self.secret_message.get('1.0', 'end-1c')
        supported_types[ext.lower()][0](self.coverPath, self.payloadText, self.frame_option.get(), self.bits_option_menu.get())
        self.save_as(ext)

    def decode_video(self):
        if self.coverPath is None:
            messagebox.showerror("Error", "Please select or drop a cover item first!")
            return
        _, ext = os.path.splitext(self.coverPath)
        text = supported_types[ext.lower()][1](self.coverPath, self.frame_option.get(), self.bits_option_menu.get())
        self.secret_message.delete('1.0', tk.END)
        self.secret_message.insert('1.0', text)

    def save_as(self, ext):
        filename = asksaveasfilename(defaultextension=ext, filetypes=[("Same as original", ext), ("All files", "*.*")])
        if filename:
            if filename.endswith(('.mp4')):
                vids.save_as(filename)



class App(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)

        self.title("I am a stegosaurus")
        self.geometry("450x700")

        container = customtkinter.CTkFrame(master=self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}
        
        for F in (MainMenu, ImagePage, DocumentPage, AudioPage, VideoPage):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
        
        self.show_frame(MainMenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


app = App()
app.mainloop()
