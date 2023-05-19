import os
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD


class MyApp:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title('Drag and Drop Files Here')

        self.label = tk.Label(self.root, text='Drag and Drop Files Here', width=50, height=5)
        self.label.pack()

        self.text_area = tk.Text(self.root, width=50, height=20)
        self.text_area.pack()

        self.label.drop_target_register(DND_FILES)
        self.label.dnd_bind('<<Drop>>', self.drop)

        self.binary_content = None

    def drop(self, event):
        file_path = event.data
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file_path)
            if ext.lower() in ['.png', '.txt', '.mp3']:  # Can specify more types here
                with open(file_path, 'rb') as file:
                    self.binary_content = file.read()
                    self.text_area.insert('1.0', str(self.binary_content))
            else:
                print(f"File type {ext} not supported.")

    def other_function(self):
        # use self.binary_content as the raw data to perform LSB
        pass

    def run(self):
        self.root.mainloop()


app = MyApp()
app.run()
