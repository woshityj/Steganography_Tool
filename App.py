import os
import tkinter as tk
from tkinter.filedialog import asksaveasfilename

import cv2
from tkinterdnd2 import DND_FILES, TkinterDnD
import image_steganography as ims

class MyApp:
    def __init__(self):
        self.encoded = None
        self.data_string = None
        self.root = TkinterDnD.Tk()
        self.root.title('Encode')

        # frame for input
        self.f_input = tk.Frame(self.root)
        self.f_input.pack()


        # input text box for entering secret
        self.lbl_secret = tk.Label(self.f_input, text='Secret message: ')
        self.lbl_secret.grid(row=0, column=0, sticky='e')
        self.tb_message = tk.Text(self.f_input, height=1, width=40)
        self.tb_message.grid(row=0, column=1)

        # specify number of LSB
        self.lbl_num = tk.Label(self.f_input, text='Number of bits: ')
        self.lbl_num.grid(row=1, column=0, sticky='e')
        self.tb_num = tk.Text(self.f_input, height=1, width=40)
        self.tb_num.grid(row=1, column=1)

        self.lbl_DND = tk.Label(self.root, text='Drag and Drop Files Here', width=50, height=5)
        self.lbl_DND.pack()

        # self.tb_debug = tk.Text(self.root, width=50, height=20)
        # self.tb_debug.pack()

        self.lbl_DND.drop_target_register(DND_FILES)
        self.lbl_DND.dnd_bind('<<Drop>>', self.drop)

        self.binary_content = None

    def drop(self, event):
        file_path = event.data
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file_path)
            if ext.lower() in ['.png']:  # Can specify more types here
                self.encoded = ims.encode(file_path, self.tb_message.get("1.0", 'end-1c'), int(self.tb_num.get("1.0", 'end-1c')))
                self.save_as(ext)
                #with open(file_path, 'rb') as file:
                #    self.binary_content = file.read()
                #    self.text_area.insert('1.0', str(self.binary_content))
            else:
                print(f"File type {ext} not supported.")

    def encode_image(self):
        # use self.binary_content as the raw data to perform LSB
        pass

    def run(self):
        self.root.mainloop()

    def save_as(self, ext):
        filename = asksaveasfilename(defaultextension=ext, filetypes=[("Same as original", ext), ("All Files", "*.*")])
        if filename:
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                cv2.imwrite(filename, self.encoded)


app = MyApp()
app.run()
