import os
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter.filedialog import asksaveasfilename
import cv2
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
        # check if number of bits specified
        try:
            num = int(self.tb_num.get("1.0", 'end-1c'))
        except ValueError:
            tk.Label(tk.Toplevel(self.root), text="Please specify the number of bits!", height=5, width=40).pack()

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
                    self.encoded = ims.encode(file_path, message, num)
                # if the file is text:
                elif ext.lower() in ['.txt']:
                    pass
                # if the file is audio:
                elif ext.lower() in ['.mp3']:
                    pass
                else:
                    tk.Label(tk.Toplevel(self.root), text=f"File type {ext} not supported.", height=5, width=40).pack()
                    return

                self.save_as(ext)
            # if tb_message is empty, do decode:
            else:
                # if the file is image:
                if ext.lower() in ['.png']:
                    self.tb_message.insert("1.0", ims.decode(file_path, num))
                # if the file is text:
                elif ext.lower() in ['.txt']:
                    pass
                # if the file is audio:
                elif ext.lower() in ['.mp3']:
                    pass
                else:
                    tk.Label(tk.Toplevel(self.root), text=f"File type {ext} not supported.", height=5, width=40).pack()
                    return

    def run(self):
        self.root.mainloop()

    def save_as(self, ext):
        filename = asksaveasfilename(defaultextension=ext, filetypes=[("Same as original", ext), ("All Files", "*.*")])
        if filename:
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                cv2.imwrite(filename, self.encoded)


app = MyApp()
app.run()
