import tkinter as tk
import tkinterdnd2 as tkdnd

def on_drop(event):
    path = event.data
    img = tk.PhotoImage(file=path)
    button.config(image=img)
    button.image = img  # Store a reference to prevent it from being garbage collected

root = tk.Tk()
root.title("Drag and Drop Images")

dnd = tkdnd.DND(root)

# Create a label that looks like a button
button = tk.Label(root, text="Drop Image Here", relief=tk.RAISED, bg="lightgray", padx=10, pady=10)
button.pack()

button.drop_target_register(tkdnd.DND_FILES)
button.dnd_bind('<<Drop>>', on_drop)

root.mainloop()
