import os, cv2, wave
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter.filedialog import asksaveasfilename
import image_steganography as ims
import audio_steganography as aus

ERROR_UNSUPPORTED_TYPE = "File type {ext} not supported."
ERROR_UNSUPPORTED_PATH = "File path {file_path} not supported. Try to use local file."

class MyApp:
    def __init__(self):
        self.encoded = None
        self.data_string = None
        self.root = TkinterDnD.Tk()
        self.root.title('LSB Steganography')
        self.root.resizable(0, 0)

        # frame for input
        self.f_input = tk.Frame(self.root)
        self.f_input.pack(padx=10, pady=10)

        # input text box for entering secret
        self.lbl_secret = tk.Label(self.f_input, text='Secret message: ')
        self.lbl_secret.grid(row=0, column=0, sticky='ne')
        self.tb_message = tk.Text(self.f_input, height=2, width=30)
        self.tb_message.grid(row=0, column=1, sticky='w')

        # specify number of LSB
        self.lbl_num = tk.Label(self.f_input, text='Number of bits: ')
        self.lbl_num.grid(row=1, column=0, sticky='e')
        self.sb_num = tk.Spinbox(self.f_input, from_=1, to=3, width=10)
        self.sb_num.grid(row=1, column=1, sticky='w')

        self.lbl_DND = tk.Label(self.root, text='Drag and Drop Files Here', width=50, height=5, bg="#c8cfdb")
        self.lbl_DND.pack(pady=10, padx=10)

        self.lbl_DND.drop_target_register(DND_FILES)
        self.lbl_DND.dnd_bind('<<Drop>>', self.drop)

        self.binary_content = None

    def drop(self, event):
        file_path = event.data
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file_path)  # ext is the extension name

            # determine to encode or decode
            # by checking whether the message text box is empty
            # if tb_message is not empty, do encode:
            message = self.tb_message.get("1.0", 'end-1c')
            if message != "":
                # if the file is image:
                if ext.lower() in ['.png']:
                    self.encoded = ims.encode(file_path, message, int(self.sb_num.get()))
                # if the file is text:
                elif ext.lower() in ['.txt']:
                    pass
                # if the file is audio:
                elif ext.lower() in ['.mp3'] or ext.lower() in ['.wav']:
                    self.audio_path = file_path
                    self.encoded = aus.encode_aud_data(file_path,message)
                else:
                    tk.Label(tk.Toplevel(self.root), text=ERROR_UNSUPPORTED_TYPE, height=5, width=40).pack()
                    return

                self.save_as(ext)
            # if tb_message is empty, do decode:
            else:
                # if the file is image:
                if ext.lower() in ['.png']:
                    self.tb_message.insert("1.0", ims.decode(file_path, int(self.sb_num.get())))
                # if the file is text:
                elif ext.lower() in ['.txt']:
                    pass
                # if the file is audio:
                elif ext.lower() in ['.mp3'] or ext.lower() in ['.wav']:
                    self.tb_message.insert("1.0", aus.decode_aud_data(file_path))
                else:
                    tk.Label(tk.Toplevel(self.root), text=f"File type {ext} not supported.", height=5, width=40).pack()
                    return
        else:
            tk.Label(tk.Toplevel(self.root), text=ERROR_UNSUPPORTED_PATH,
                     height=5, width=50, justify='left', wraplength=350).pack(anchor='w', padx=10, pady=10)

    def run(self):
        self.root.mainloop()

    def save_as(self, ext):
        # save as prompt
        filename = asksaveasfilename(defaultextension=ext, filetypes=[("Same as original", ext), ("All Files", "*.*")])
        if filename:
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                # save image
                cv2.imwrite(filename, self.encoded)
                # show image as per requested in spec
                cv2.imshow(filename, self.encoded)
            elif filename.endswith(('.wav', '.mp3')):
                song = wave.open(self.audio_path, mode = 'rb')
                with wave.open(filename, 'wb') as fd:
                    fd.setparams(song.getparams())
                    fd.writeframes(self.encoded)
                    print("\nEncoded the data successfully in the audio file")


app = MyApp()
app.run()
