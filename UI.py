import tkinter as tk
from tkinter import PhotoImage, Text, Scrollbar, Button, Label
import time

import AI_loader

class MyLittleAIOfficeUI:
    def __init__(self, root):
        self.root = root
        root.title("My Little AI Office")
        root.geometry("1600x800")  # Set the window size
        
        # Configure rows and columns for proper scaling
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(4, weight=1)
        
        # Title Label
        self.title_label = Label(root, text="My Little AI Office", font=("Arial", 20))
        self.title_label.grid(row=0, column=0, sticky="W")
        
        # Time Label
        self.time_label = Label(root, text="", font=("Arial", 12))
        self.time_label.grid(row=0, column=4, sticky="E")
        self.update_time()
        
        # First Image
        self.image1 = PhotoImage(file="path_to_your_first_image.png")  # Update this path
        self.image_label1 = Label(root, image=self.image1)
        self.image_label1.grid(row=1, column=0, sticky="nw")
        
        # First Text Box with Scroll
        self.text1 = Text(root, wrap="word", height=20, width=67)
        self.scroll1 = Scrollbar(root, command=self.text1.yview)
        self.text1.configure(yscrollcommand=self.scroll1.set)
        self.text1.grid(row=1, column=1, sticky="nsew")
        self.scroll1.grid(row=1, column=2, sticky="nsew")
        
        # Second Image
        self.image2 = PhotoImage(file="path_to_your_second_image.png")  # Update this path
        self.image_label2 = Label(root, image=self.image2)
        self.image_label2.grid(row=1, column=3, sticky="nw")
        
        # Second Text Box with Scroll
        self.text2 = Text(root, wrap="word", height=20, width=67)
        self.scroll2 = Scrollbar(root, command=self.text2.yview)
        self.text2.configure(yscrollcommand=self.scroll2.set)
        self.text2.grid(row=1, column=4, sticky="nsew")
        self.scroll2.grid(row=1, column=5, sticky="nsew")
        
        # Bottom Right Button
        self.submit_button = Button(root, text="Pause", command=self.on_submit)
        self.submit_button.grid(row=2, column=4, sticky="E")

    def update_image1(self, new_path):
        new_image = PhotoImage(file=new_path)
        self.image_label1.configure(image=new_image)
        self.image_label1.image = new_image
    
    def update_image2(self, new_path):
        new_image = PhotoImage(file=new_path)
        self.image_label2.configure(image=new_image)
        self.image_label2.image = new_image

    def update_text1(self, new_text):
        self.text1.delete("1.0", tk.END)
        self.text1.insert(tk.END, new_text)

    def update_text2(self, new_text):
        self.text2.delete("1.0", tk.END)
        self.text2.insert(tk.END, new_text)
    
    def on_submit(self):
        # Define what happens when the submit button is clicked
        print("Pause button clicked")
        AI_loader.pause = (AI_loader.pause == False)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)  # Update the time every second

app = None

def start_UI():
    global app
    root = tk.Tk()
    app = MyLittleAIOfficeUI(root)

    AI_loader.app = app

    root.mainloop()

